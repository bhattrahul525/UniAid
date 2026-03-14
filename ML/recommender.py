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

    @property
    def mentors_csv(self) -> Path:
        return self.data_dir / "mentors.csv"

    @property
    def users_csv(self) -> Path:
        return self.data_dir / "users.csv"

    @property
    def interactions_csv(self) -> Path:
        return self.data_dir / "interactions.csv"

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
    Matches mentors.csv columns:
    mentor_id, first_name, last_name, mentor_type, university, field_of_study, degree_level,
    years_in_country, visa_experience, housing_experience, cultural_adaptation_experience,
    career_guidance_experience, languages_spoken, availability_hours_per_week, sessions_completed,
    response_time_hours, graduation_year, mentor_rating
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
        f"languages: {_safe_str(row.get('languages_spoken'))}",
        f"can help with: {', '.join(help_tags)}" if help_tags else "",
        f"sessions completed: {_safe_str(row.get('sessions_completed'))}",
        f"response time hours: {_safe_str(row.get('response_time_hours'))}",
        f"mentor rating: {_safe_str(row.get('mentor_rating'))}",
        f"graduation year: {_safe_str(row.get('graduation_year'))}",
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


def compute_mentor_quality(interactions_df: pd.DataFrame, mentors_df: pd.DataFrame) -> pd.DataFrame:
    """
    Build a per-mentor quality table from interactions.csv.
    Columns expected:
    interaction_id,user_id,mentor_id,interaction_type,session_duration_minutes,rating_given_by_user,
    helpfulness_score,match_success
    """
    if interactions_df.empty:
        out = mentors_df[["mentor_id"]].copy()
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
    out = mentors_df[["mentor_id"]].merge(agg[["mentor_id", "interaction_count", "success_rate", "avg_helpfulness", "avg_user_rating", "quality_score"]],
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

    def load_dataframes(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        mentors_df = pd.read_csv(self.paths.mentors_csv)
        users_df = pd.read_csv(self.paths.users_csv)
        interactions_df = pd.read_csv(self.paths.interactions_csv)
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
        self._mentor_embeddings = np.load(self.paths.mentor_embeddings_npy)
        self._nn = joblib.load(self.paths.nn_index_joblib)

        if self.paths.mentor_quality_joblib.exists():
            self._mentor_quality_df = joblib.load(self.paths.mentor_quality_joblib)
        else:
            # Recompute quickly if missing
            interactions_df = pd.read_csv(self.paths.interactions_csv)
            self._mentor_quality_df = compute_mentor_quality(interactions_df, self._mentors_df)

    def _load_users_df(self) -> pd.DataFrame:
        if self._users_df is None:
            self._users_df = pd.read_csv(self.paths.users_csv)
        return self._users_df

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
        w_similarity: float = 0.85,
        w_quality: float = 0.15,
    ) -> List[Dict[str, Any]]:
        """
        Returns a ranked list of mentors with scores.

        - Uses semantic similarity (cosine) between (user profile + request) and mentors.
        - Applies a small interactions-based boost via quality_score.
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

        model = self._load_model()
        q_emb = model.encode([query_text], normalize_embeddings=True)

        pool = max(top_k, min(candidate_pool, len(self._mentors_df)))
        distances, indices = self._nn.kneighbors(q_emb, n_neighbors=pool)
        idxs = indices[0]
        dists = distances[0]
        sim = 1.0 - dists

        candidates = self._mentors_df.iloc[idxs].copy()
        candidates["similarity"] = sim
        candidates = candidates.merge(self._mentor_quality_df[["mentor_id", "quality_score", "interaction_count", "success_rate", "avg_helpfulness", "avg_user_rating"]],
                                      on="mentor_id", how="left")
        for col in ["quality_score", "interaction_count", "success_rate", "avg_helpfulness", "avg_user_rating"]:
            candidates[col] = candidates[col].fillna(0)

        candidates["final_score"] = (w_similarity * candidates["similarity"]) + (w_quality * candidates["quality_score"])
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
            "languages_spoken",
            "availability_hours_per_week",
            "sessions_completed",
            "response_time_hours",
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


if __name__ == "__main__":
    import sys

    # Default paths: data in UniAid/Data, models in UniAid/Backend/ML/models
    _base = Path(__file__).resolve().parent  # UniAid/Backend/ML
    _paths = RecommenderPaths(data_dir=_base.parent.parent / "Data", models_dir=_base / "models")

    if len(sys.argv) >= 2 and sys.argv[1] == "build":
        rec = MentorRecommender(paths=_paths)
        rec.build_and_persist_index()
        print("Index built. Artifacts saved under models/")
    else:
        print("Usage: python recommender.py build")
        print("  Then start the API: uvicorn api:app --reload --port 8000")

