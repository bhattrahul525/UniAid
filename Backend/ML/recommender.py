from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import joblib
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors


@dataclass(frozen=True)
class RecommenderPaths:
    data_dir: Path
    models_dir: Path
    mentors_csv_name: str = "mentors.csv"
    users_csv_name: str = "users.csv"
    interactions_csv_name: str = "interactions.csv"

    @property
    def mentors_csv(self) -> Path:
        return self.data_dir / self.mentors_csv_name

    @property
    def users_csv(self) -> Path:
        return self.data_dir / self.users_csv_name

    @property
    def interactions_csv(self) -> Path:
        return self.data_dir / self.interactions_csv_name

    @property
    def mentor_df_joblib(self) -> Path:
        return self.models_dir / "mentors_df.joblib"

    @property
    def mentor_embeddings_npy(self) -> Path:
        return self.models_dir / "mentor_embeddings.npy"

    @property
    def nn_index_joblib(self) -> Path:
        return self.models_dir / "mentor_nn.joblib"

    @property
    def mentor_quality_joblib(self) -> Path:
        return self.models_dir / "mentor_quality.joblib"


def _safe_str(x: Any) -> str:
    if x is None:
        return ""
    if isinstance(x, float) and np.isnan(x):
        return ""
    s = str(x).strip()
    if s.upper() == "NULL":
        return ""
    return s


def _flag_label(name: str, value: Any) -> Optional[str]:
    s = _safe_str(value)
    if s == "":
        return None
    # Your CSVs use 0/1 for many fields.
    if s in {"1", "true", "True", "YES", "yes"}:
        return name
    return None


def mentor_to_text(row: pd.Series) -> str:
    """
    Convert a mentor row into a text document for semantic embedding.
    Works with both the original mentors.csv and the richer mentors_dataset.csv
    that include mentoring_topics and bio.
    """
    help_tags = [
        _flag_label("visa", row.get("visa_experience")),
        _flag_label("housing", row.get("housing_experience")),
        _flag_label("cultural adaptation", row.get("cultural_adaptation_experience")),
        _flag_label("career guidance", row.get("career_guidance_experience")),
    ]
    help_tags = [t for t in help_tags if t]

    parts = [
        f"mentor type: {_safe_str(row.get('mentor_type'))}",
        f"university: {_safe_str(row.get('university'))}",
        f"field of study: {_safe_str(row.get('field_of_study'))}",
        f"degree level: {_safe_str(row.get('degree_level'))}",
        f"years in country: {_safe_str(row.get('years_in_country'))}",
        f"mentoring topics: {_safe_str(row.get('mentoring_topics'))}",
        f"languages: {_safe_str(row.get('languages_spoken'))}",
        f"can help with: {', '.join(help_tags)}" if help_tags else "",
        f"sessions completed: {_safe_str(row.get('sessions_completed'))}",
        f"response time hours: {_safe_str(row.get('response_time_hours'))}",
        f"mentor rating: {_safe_str(row.get('mentor_rating'))}",
        f"graduation year: {_safe_str(row.get('graduation_year'))}",
        f"bio: {_safe_str(row.get('bio'))}",
    ]
    return ". ".join([p for p in parts if p])


def user_profile_to_text(user: Dict[str, Any]) -> str:
    """
    Convert a user profile dict (users.csv columns) into a text document.
    """
    concerns = [
        _flag_label("visa", user.get("concern_visa")),
        _flag_label("accommodation", user.get("concern_accommodation")),
        _flag_label("safety", user.get("concern_safety")),
        _flag_label("academics", user.get("concern_academics")),
        _flag_label("career", user.get("concern_career")),
        _flag_label("culture", user.get("concern_culture")),
    ]
    concerns = [c for c in concerns if c]

    parts = [
        f"user type: {_safe_str(user.get('user_type'))}",
        f"home country: {_safe_str(user.get('home_country'))}",
        f"preferred city type: {_safe_str(user.get('preferred_city_type'))}",
        f"target university: {_safe_str(user.get('target_university'))}",
        f"field of study: {_safe_str(user.get('field_of_study'))}",
        f"degree level: {_safe_str(user.get('degree_level'))}",
        f"intended start year: {_safe_str(user.get('intended_start_year'))}",
        f"budget range aud: {_safe_str(user.get('budget_range_aud'))}",
        f"scholarship interest: {_safe_str(user.get('scholarship_interest'))}",
        f"preferred language: {_safe_str(user.get('preferred_language'))}",
        f"accommodation type: {_safe_str(user.get('accommodation_type'))}",
        f"work while studying interest: {_safe_str(user.get('work_while_studying_interest'))}",
        f"concerns: {', '.join(concerns)}" if concerns else "",
    ]
    return ". ".join([p for p in parts if p])


def build_user_request_text(
    *,
    user_profile: Optional[Dict[str, Any]] = None,
    request_text: Optional[str] = None,
) -> str:
    base = user_profile_to_text(user_profile) if user_profile else ""
    req = _safe_str(request_text)
    if base and req:
        return f"{base}. request: {req}"
    if req:
        return f"request: {req}"
    return base


def _minmax_0_1(series: pd.Series) -> pd.Series:
    s = series.astype(float)
    mn = float(s.min()) if len(s) else 0.0
    mx = float(s.max()) if len(s) else 0.0
    if mx - mn < 1e-9:
        return pd.Series(np.zeros(len(s)), index=s.index, dtype=float)
    return (s - mn) / (mx - mn)


def _normalize_interactions_user_id(interactions_df: pd.DataFrame) -> pd.DataFrame:
    """If interactions use mentee_id instead of user_id, add user_id for recommender logic."""
    if interactions_df.empty:
        return interactions_df
    if "user_id" not in interactions_df.columns and "mentee_id" in interactions_df.columns:
        interactions_df = interactions_df.copy()
        interactions_df["user_id"] = interactions_df["mentee_id"]
    return interactions_df


def compute_mentor_quality(interactions_df: pd.DataFrame, mentors_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a per-mentor quality table from interactions.csv.
    mentors_df must have mentor_id (or id, then we use id as mentor_id).
    """
    mdf = mentors_df.copy()
    if "mentor_id" not in mdf.columns and "id" in mdf.columns:
        mdf["mentor_id"] = mdf["id"]
    if interactions_df.empty:
        out = mdf[["mentor_id"]].copy()
        out["interaction_count"] = 0
        out["success_rate"] = 0.0
        out["avg_helpfulness"] = 0.0
        out["avg_user_rating"] = 0.0
        out["quality_score"] = 0.0
        return out

    g = interactions_df.groupby("mentor_id", dropna=False)
    agg = g.agg(
        interaction_count=("interaction_id", "count"),
        success_rate=("match_success", "mean"),
        avg_helpfulness=("helpfulness_score", "mean"),
        avg_user_rating=("rating_given_by_user", "mean"),
    ).reset_index()

    # Normalize components for stable weighting
    agg["interaction_count_norm"] = _minmax_0_1(agg["interaction_count"])
    agg["success_rate_norm"] = _minmax_0_1(agg["success_rate"])
    agg["avg_helpfulness_norm"] = _minmax_0_1(agg["avg_helpfulness"].fillna(0))
    agg["avg_user_rating_norm"] = _minmax_0_1(agg["avg_user_rating"].fillna(0))

    # Simple, hackathon-friendly quality signal
    agg["quality_score"] = (
        0.35 * agg["success_rate_norm"]
        + 0.25 * agg["avg_helpfulness_norm"]
        + 0.25 * agg["avg_user_rating_norm"]
        + 0.15 * agg["interaction_count_norm"]
    )

    # Ensure every mentor_id exists (fill missing with zeros)
    out = mdf[["mentor_id"]].merge(agg[["mentor_id", "interaction_count", "success_rate", "avg_helpfulness", "avg_user_rating", "quality_score"]],
                                  on="mentor_id", how="left")
    for col in ["interaction_count", "success_rate", "avg_helpfulness", "avg_user_rating", "quality_score"]:
        out[col] = out[col].fillna(0)
    out["interaction_count"] = out["interaction_count"].astype(int)
    return out


class MentorRecommender:
    def __init__(
        self,
        *,
        paths: RecommenderPaths,
        model_name: str = "all-MiniLM-L6-v2",
    ) -> None:
        self.paths = paths
        self.model_name = model_name
        self.paths.models_dir.mkdir(parents=True, exist_ok=True)

        self._model: Optional[SentenceTransformer] = None
        self._mentors_df: Optional[pd.DataFrame] = None
        self._users_df: Optional[pd.DataFrame] = None
        self._mentor_quality_df: Optional[pd.DataFrame] = None
        self._mentor_embeddings: Optional[np.ndarray] = None
        self._nn: Optional[NearestNeighbors] = None

    def _normalize_mentors_df(self, mentors_df: pd.DataFrame) -> pd.DataFrame:
        """Ensure mentors_df has mentor_id (mentors.csv may use 'id' as primary key)."""
        df = mentors_df.copy()
        if "mentor_id" not in df.columns and "id" in df.columns:
            df["mentor_id"] = df["id"]
        return df

    def load_dataframes(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        mentors_df = pd.read_csv(self.paths.mentors_csv)
        mentors_df = self._normalize_mentors_df(mentors_df)
        users_df = pd.read_csv(self.paths.users_csv)
        interactions_df = pd.read_csv(self.paths.interactions_csv)
        interactions_df = _normalize_interactions_user_id(interactions_df)
        return mentors_df, users_df, interactions_df

    def _load_model(self) -> SentenceTransformer:
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model

    def build_and_persist_index(self) -> None:
        mentors_df, _, interactions_df = self.load_dataframes()
        mentors_df = mentors_df.copy()
        mentors_df["text_repr"] = mentors_df.apply(mentor_to_text, axis=1)

        model = self._load_model()
        embeddings = model.encode(
            mentors_df["text_repr"].tolist(),
            normalize_embeddings=True,
            show_progress_bar=True,
        )

        nn = NearestNeighbors(metric="cosine")
        nn.fit(embeddings)

        mentor_quality_df = compute_mentor_quality(interactions_df, mentors_df)

        joblib.dump(mentors_df, self.paths.mentor_df_joblib)
        np.save(self.paths.mentor_embeddings_npy, embeddings)
        joblib.dump(nn, self.paths.nn_index_joblib)
        joblib.dump(mentor_quality_df, self.paths.mentor_quality_joblib)

    def _load_index_artifacts(self) -> None:
        if self._mentors_df is not None and self._mentor_embeddings is not None and self._nn is not None:
            return

        if not (self.paths.mentor_df_joblib.exists() and self.paths.mentor_embeddings_npy.exists() and self.paths.nn_index_joblib.exists()):
            self.build_and_persist_index()

        self._mentors_df = joblib.load(self.paths.mentor_df_joblib)
        self._mentors_df = self._normalize_mentors_df(self._mentors_df)
        self._mentor_embeddings = np.load(self.paths.mentor_embeddings_npy)
        self._nn = joblib.load(self.paths.nn_index_joblib)

        if self.paths.mentor_quality_joblib.exists():
            self._mentor_quality_df = joblib.load(self.paths.mentor_quality_joblib)
        else:
            # Recompute quickly if missing
            interactions_df = pd.read_csv(self.paths.interactions_csv)
            interactions_df = _normalize_interactions_user_id(interactions_df)
            self._mentor_quality_df = compute_mentor_quality(interactions_df, self._mentors_df)

    def _load_users_df(self) -> pd.DataFrame:
        if self._users_df is None:
            self._users_df = pd.read_csv(self.paths.users_csv)
        return self._users_df

    def _get_user_past_mentor_ids(self, user_id: int) -> set[int]:
        """Return set of mentor_ids this user has interacted with (from interactions.csv)."""
        interactions_df = pd.read_csv(self.paths.interactions_csv)
        interactions_df = _normalize_interactions_user_id(interactions_df)
        if interactions_df.empty or "user_id" not in interactions_df.columns or "mentor_id" not in interactions_df.columns:
            return set()
        subset = interactions_df.loc[interactions_df["user_id"] == user_id, "mentor_id"]
        return set(int(x) for x in subset.dropna().unique())

    def get_user_profile(self, user_id: int) -> Dict[str, Any]:
        users_df = self._load_users_df()
        row = users_df.loc[users_df["user_id"] == user_id]
        if row.empty:
            raise ValueError(f"user_id {user_id} not found in users.csv")
        return row.iloc[0].to_dict()

    def recommend(
        self,
        *,
        user_id: Optional[int] = None,
        user_profile: Optional[Dict[str, Any]] = None,
        request_text: Optional[str] = None,
        top_k: int = 5,
        candidate_pool: int = 50,
        w_similarity: float = 0.65,
        w_quality: float = 0.15,
        w_past_interaction: float = 0.35,
        candidate_university: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Returns a ranked list of mentors with scores.
        - If candidate_university is set, only mentors from that university are considered (search within subset).
        - Uses semantic similarity (cosine) between (user profile + request) and mentors.
        """
        self._load_index_artifacts()
        assert self._mentors_df is not None
        assert self._mentor_embeddings is not None
        assert self._nn is not None
        assert self._mentor_quality_df is not None

        if user_profile is None and user_id is not None:
            user_profile = self.get_user_profile(user_id)

        query_text = build_user_request_text(user_profile=user_profile, request_text=request_text)
        if not query_text:
            raise ValueError("Provide at least one of: user_id, user_profile, request_text")

        past_mentor_ids: set[int] = set()
        if user_id is not None:
            past_mentor_ids = self._get_user_past_mentor_ids(user_id)

        model = self._load_model()
        q_emb = model.encode([query_text], normalize_embeddings=True)

        if candidate_university and "university" in self._mentors_df.columns:
            # Filter mentors to this university first, then run recommendation on the filtered list only.
            u_lower = candidate_university.strip().lower()
            uni_series = self._mentors_df["university"].fillna("").astype(str).str.strip().str.lower()
            uni_mask = uni_series == u_lower
            university_indices = np.where(uni_mask)[0]
            if len(university_indices) == 0:
                return []
            subset_embeddings = self._mentor_embeddings[university_indices]
            n_take = min(top_k, len(university_indices))
            nn_subset = NearestNeighbors(metric="cosine")
            nn_subset.fit(subset_embeddings)
            dists, local_idx = nn_subset.kneighbors(q_emb, n_neighbors=n_take)
            dists = dists[0]
            local_idx = local_idx[0]
            idxs = university_indices[local_idx]
            sim = 1.0 - dists
            candidates = self._mentors_df.iloc[idxs].copy()
            candidates["similarity"] = sim
        else:
            pool = max(top_k, min(candidate_pool, len(self._mentors_df)))
            distances, indices = self._nn.kneighbors(q_emb, n_neighbors=pool)
            idxs = indices[0]
            dists = distances[0]
            sim = 1.0 - dists
            candidates = self._mentors_df.iloc[idxs].copy()
            candidates["similarity"] = sim

        # Include mentors the user has interacted with if not already in semantic pool
        if past_mentor_ids:
            in_pool = set(candidates["mentor_id"].astype(int))
            u_lower = candidate_university.strip().lower() if candidate_university else None
            for mid in past_mentor_ids:
                if mid in in_pool:
                    continue
                row = self._mentors_df[self._mentors_df["mentor_id"] == mid]
                if row.empty:
                    continue
                if u_lower and "university" in row.columns:
                    row_uni = (row["university"].iloc[0] or "").strip().lower()
                    if row_uni != u_lower:
                        continue
                extra = row.copy()
                extra["similarity"] = 0.0
                candidates = pd.concat([candidates, extra], ignore_index=True)
                in_pool.add(mid)

        candidates = candidates.drop_duplicates(subset=["mentor_id"], keep="first")
        candidates = candidates.merge(
            self._mentor_quality_df[["mentor_id", "quality_score", "interaction_count", "success_rate", "avg_helpfulness", "avg_user_rating"]],
            on="mentor_id",
            how="left",
        )
        for col in ["quality_score", "interaction_count", "success_rate", "avg_helpfulness", "avg_user_rating"]:
            candidates[col] = candidates[col].fillna(0)

        candidates["past_interaction"] = candidates["mentor_id"].astype(int).isin(past_mentor_ids).astype(float)
        candidates["final_score"] = (
            w_similarity * candidates["similarity"]
            + w_quality * candidates["quality_score"]
            + w_past_interaction * candidates["past_interaction"]
        )
        candidates = candidates.sort_values(["final_score", "similarity"], ascending=False).head(top_k)

        # Return only what the frontend needs to display choices
        out_cols = [
            "mentor_id",
            "first_name",
            "last_name",
            "mentor_type",
            "university",
            "field_of_study",
            "degree_level",
            "mentoring_topics",
            "languages_spoken",
            "availability_hours_per_week",
            "sessions_completed",
            "response_time_hours",
            "bio",
            "mentor_rating",
            "similarity",
            "quality_score",
            "final_score",
            "interaction_count",
            "success_rate",
        ]
        out_cols = [c for c in out_cols if c in candidates.columns]
        records = candidates[out_cols].to_dict(orient="records")

        # Convert numpy types to plain Python types for JSON friendliness
        def _py(x: Any) -> Any:
            if isinstance(x, (np.floating, np.integer)):
                return x.item()
            return x

        return [{k: _py(v) for k, v in r.items()} for r in records]

    def evaluate(
        self,
        *,
        sample_size: Optional[int] = 200,
        top_k: int = 5,
        seed: int = 42,
    ) -> Dict[str, Any]:
        """
        Simple offline evaluation: for (user_id, mentor_id) in interactions,
        get recommendations for user_id and check if mentor_id is in top_k.
        Returns hit_rate_at_k and mean_reciprocal_rank.
        """
        self._load_index_artifacts()
        self._load_users_df()
        interactions_df = pd.read_csv(self.paths.interactions_csv)
        interactions_df = _normalize_interactions_user_id(interactions_df)
        if interactions_df.empty:
            return {"hit_rate_at_k": 0.0, "mrr": 0.0, "n_eval": 0, "top_k": top_k}

        eval_df = interactions_df[["user_id", "mentor_id"]].drop_duplicates()
        if sample_size and len(eval_df) > sample_size:
            rng = np.random.default_rng(seed)
            eval_df = eval_df.sample(n=sample_size, random_state=rng)
        hits = 0
        mrr_sum = 0.0
        n = 0
        for _, row in eval_df.iterrows():
            uid, true_mid = int(row["user_id"]), int(row["mentor_id"])
            try:
                recs = self.recommend(user_id=uid, top_k=top_k, candidate_pool=min(100, len(self._mentors_df)))
                rec_mids = [int(r["mentor_id"]) for r in recs]
                if true_mid in rec_mids:
                    hits += 1
                    rank = rec_mids.index(true_mid) + 1
                    mrr_sum += 1.0 / rank
            except (ValueError, KeyError):
                continue
            n += 1
        return {
            "hit_rate_at_k": round(hits / n, 4) if n else 0.0,
            "mrr": round(mrr_sum / n, 4) if n else 0.0,
            "n_eval": n,
            "top_k": top_k,
        }


if __name__ == "__main__":
    import sys

    # Default paths: data in UniAid/Dataset, models in UniAid/Backend/ML/models
    _base = Path(__file__).resolve().parent  # UniAid/Backend/ML
    _paths = RecommenderPaths(
        data_dir=_base.parent.parent / "Dataset",
        models_dir=_base / "models",
        mentors_csv_name="mentors_dataset.csv",
        users_csv_name="mentees_dataset.csv",
        interactions_csv_name="interactions_dataset.csv",
    )

    if len(sys.argv) >= 2 and sys.argv[1] == "build":
        rec = MentorRecommender(paths=_paths)
        rec.build_and_persist_index()
        print("Index built. Artifacts saved under models/")
    else:
        print("Usage: python recommender.py build")
        print("  Then start the API: uvicorn main:app --reload --port 8000 (from Backend)")

