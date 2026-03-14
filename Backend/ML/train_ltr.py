"""
Train the Learning-to-Rank (LTR) model for mentor recommendation.

Builds training data from interactions: (mentee_id, mentor_id) pairs with labels
(match_success or graded relevance). For each mentee, adds sampled negative
mentors. Features: similarity, quality_score, explicit matches, etc.
Trains LightGBM LambdaRank and saves to ML/models/.

Run from Backend/:  python -m ML.train_ltr
Or from Backend/ML/: python train_ltr.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

# Ensure ML directory is on path
_ML_DIR = Path(__file__).resolve().parent
if str(_ML_DIR) not in sys.path:
    sys.path.insert(0, str(_ML_DIR))

from ltr import (
    LTR_FEATURE_NAMES,
    build_ltr_features_row,
    save_ltr_model,
    train_ltr,
)
from recommender import (
    RecommenderPaths,
    _normalize_interactions_user_id,
    build_user_request_text,
    compute_mentor_quality,
    mentor_to_text,
    user_profile_to_text,
)


def _minmax_0_1(series: pd.Series) -> pd.Series:
    s = series.astype(float)
    mn = float(s.min()) if len(s) else 0.0
    mx = float(s.max()) if len(s) else 0.0
    if mx - mn < 1e-9:
        return pd.Series(np.zeros(len(s)), index=s.index, dtype=float)
    return (s - mn) / (mx - mn)


def load_data(paths: RecommenderPaths):
    """Load mentors, users (mentees), interactions and ensure mentor_id / user_id."""
    mentors_df = pd.read_csv(paths.mentors_csv)
    if "mentor_id" not in mentors_df.columns and "id" in mentors_df.columns:
        mentors_df["mentor_id"] = mentors_df["id"]
    users_df = pd.read_csv(paths.users_csv)
    if "user_id" not in users_df.columns and "mentee_id" in users_df.columns:
        users_df["user_id"] = users_df["mentee_id"]
    interactions_df = pd.read_csv(paths.interactions_csv)
    interactions_df = _normalize_interactions_user_id(interactions_df)
    return mentors_df, users_df, interactions_df


def build_training_data(
    mentors_df: pd.DataFrame,
    users_df: pd.DataFrame,
    interactions_df: pd.DataFrame,
    mentor_embeddings: np.ndarray,
    mentor_quality_df: pd.DataFrame,
    embedding_model,
    *,
    negatives_per_user: int = 15,
    use_rating_as_label: bool = True,
    random_state: int = 42,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Build X (features), y (relevance), group (sizes per user).
    Positive pairs: (user_id, mentor_id) from interactions with label from match_success or rating.
    Negative pairs: for each user, sample mentors they did not interact with, label 0.
    """
    # Mentor index by mentor_id (row index in mentors_df and mentor_embeddings; must match length)
    n_emb = len(mentor_embeddings)
    mentor_id_to_idx = {}
    for i, mid in enumerate(mentors_df["mentor_id"].astype(int)):
        if i < n_emb:
            mentor_id_to_idx[mid] = i

    # User profiles by user_id
    users_df = users_df.copy()
    if "user_id" not in users_df.columns:
        users_df["user_id"] = users_df.index
    user_profiles = {}
    for _, row in users_df.iterrows():
        uid = int(row["user_id"])
        user_profiles[uid] = row.to_dict()

    # User embeddings: for each user_id we need one embedding (from profile text)
    user_embeddings = {}
    for uid in interactions_df["user_id"].astype(int).unique():
        if uid not in user_profiles:
            continue
        profile = user_profiles[uid]
        text = user_profile_to_text(profile)
        if not text.strip():
            continue
        emb = embedding_model.encode([text], normalize_embeddings=True)
        user_embeddings[uid] = emb[0]

    quality_by_id = mentor_quality_df.set_index("mentor_id").to_dict(orient="index")
    rating_max = 5.0
    if "mentor_rating" in mentors_df.columns:
        rmax = mentors_df["mentor_rating"].max()
        if pd.notna(rmax) and float(rmax) >= 1:
            rating_max = float(rmax)
    interaction_count_max = 200.0
    if "interaction_count" in mentor_quality_df.columns:
        imax = mentor_quality_df["interaction_count"].max()
        if pd.notna(imax) and float(imax) >= 1:
            interaction_count_max = float(imax)
    availability_max = 20.0
    if "availability_hours_per_week" in mentors_df.columns:
        amax = mentors_df["availability_hours_per_week"].max()
        if pd.notna(amax) and float(amax) >= 1:
            availability_max = float(amax)
    response_time_max = 72.0

    # Mentor rows as dicts (with quality merged for convenience)
    mq = mentor_quality_df.set_index("mentor_id")
    qcols = [c for c in ["quality_score", "success_rate", "interaction_count"] if c in mq.columns]
    mentors_with_quality = mentors_df.merge(
        mq[qcols] if qcols else mq,
        left_on="mentor_id",
        right_index=True,
        how="left",
    )
    for col in ["quality_score", "success_rate", "interaction_count"]:
        if col in mentors_with_quality.columns:
            mentors_with_quality[col] = mentors_with_quality[col].fillna(0)

    all_mentor_ids = set(mentors_df["mentor_id"].astype(int))
    rng = np.random.default_rng(random_state)

    # Collect (user_id, mentor_id, label) and features
    groups = []
    X_list = []
    y_list = []

    for user_id in interactions_df["user_id"].astype(int).unique():
        if user_id not in user_embeddings or user_id not in user_profiles:
            continue
        u_emb = user_embeddings[user_id]
        profile = user_profiles[user_id]
        user_positive_mentors = set(
            interactions_df.loc[interactions_df["user_id"] == user_id, "mentor_id"].astype(int)
        )
        group_count = 0
        # Positives with label
        for _, int_row in interactions_df[interactions_df["user_id"] == user_id].iterrows():
            mentor_id = int(int_row["mentor_id"])
            if mentor_id not in mentor_id_to_idx:
                continue
            if use_rating_as_label:
                # Graded relevance: 0-1 from rating and match_success
                rating = float(int_row.get("rating_given_by_user", 0))
                match_ok = float(int_row.get("match_success", 0))
                label = (rating / 5.0) * 0.5 + match_ok * 0.5  # [0, 1]
            else:
                label = float(int_row.get("match_success", 0))

            idx = mentor_id_to_idx[mentor_id]
            sim = 1.0 - _cosine_distance(u_emb, mentor_embeddings[idx])
            mentor_row = mentors_with_quality[mentors_with_quality["mentor_id"] == mentor_id].iloc[0].to_dict()
            mentor_quality = quality_by_id.get(mentor_id, {})
            if not isinstance(mentor_quality, dict):
                mentor_quality = {}

            feat = build_ltr_features_row(
                similarity=sim,
                quality_score=float(mentor_row.get("quality_score", 0.0)),
                past_interaction=1.0,
                mentor=mentor_row,
                mentor_quality=mentor_quality,
                request_text=None,
                user_profile=profile,
                university_from_query=profile.get("target_university"),
                rating_max=rating_max,
                interaction_count_max=interaction_count_max,
                availability_max=availability_max,
                response_time_max=response_time_max,
            )
            X_list.append(feat)
            y_list.append(label)
            group_count += 1

        # Negatives (only from mentors in our index)
        neg_pool = list(all_mentor_ids - user_positive_mentors)
        neg_pool = [m for m in neg_pool if m in mentor_id_to_idx]
        if len(neg_pool) > negatives_per_user:
            neg_ids = rng.choice(neg_pool, size=negatives_per_user, replace=False)
        else:
            neg_ids = neg_pool
        for mentor_id in neg_ids:
            idx = mentor_id_to_idx[mentor_id]
            sim = 1.0 - _cosine_distance(u_emb, mentor_embeddings[idx])
            mentor_row = mentors_with_quality[mentors_with_quality["mentor_id"] == mentor_id].iloc[0].to_dict()
            mentor_quality = quality_by_id.get(mentor_id, {})
            if not isinstance(mentor_quality, dict):
                mentor_quality = {}

            feat = build_ltr_features_row(
                similarity=sim,
                quality_score=float(mentor_row.get("quality_score", 0.0)),
                past_interaction=0.0,
                mentor=mentor_row,
                mentor_quality=mentor_quality,
                request_text=None,
                user_profile=profile,
                university_from_query=profile.get("target_university"),
                rating_max=rating_max,
                interaction_count_max=interaction_count_max,
                availability_max=availability_max,
                response_time_max=response_time_max,
            )
            X_list.append(feat)
            y_list.append(0.0)
            group_count += 1

        if group_count > 0:
            groups.append(group_count)

    X = np.array(X_list, dtype=np.float64)
    y = np.array(y_list, dtype=np.float64)
    group = np.array(groups, dtype=np.int32)
    return X, y, group


def _cosine_distance(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=np.float64).ravel()
    b = np.asarray(b, dtype=np.float64).ravel()
    dot = float(np.dot(a, b))
    na = float(np.linalg.norm(a))
    nb = float(np.linalg.norm(b))
    if na < 1e-12 or nb < 1e-12:
        return 1.0
    return 1.0 - (dot / (na * nb))


def main():
    base = Path(__file__).resolve().parent
    data_dir = base.parent.parent / "Dataset"
    models_dir = base / "models"
    paths = RecommenderPaths(
        data_dir=data_dir,
        models_dir=models_dir,
        mentors_csv_name="mentors_dataset.csv",
        users_csv_name="mentees_dataset.csv",
        interactions_csv_name="interactions_dataset.csv",
    )

    print("Loading data...")
    _, users_df, interactions_df = load_data(paths)
    if interactions_df.empty:
        print("No interactions; cannot train LTR. Exiting.")
        return 1

    print("Loading index artifacts (mentors_df must match embeddings row order)...")
    import joblib
    mentors_df = joblib.load(models_dir / "mentors_df.joblib")
    if "mentor_id" not in mentors_df.columns and "id" in mentors_df.columns:
        mentors_df["mentor_id"] = mentors_df["id"]
    mentor_embeddings = np.load(models_dir / "mentor_embeddings.npy")
    mentor_quality_df = joblib.load(models_dir / "mentor_quality.joblib")
    if len(mentors_df) != len(mentor_embeddings):
        print(
            f"Warning: mentors_df ({len(mentors_df)}) != embeddings ({len(mentor_embeddings)}). "
            "Using only mentors that fit in embedding array. Rebuild index for full data."
        )
        mentors_df = mentors_df.iloc[: len(mentor_embeddings)].copy()

    print("Loading embedding model...")
    from sentence_transformers import SentenceTransformer
    model_name = "all-MiniLM-L6-v2"
    embedding_model = SentenceTransformer(model_name)

    print("Building training data (positives + sampled negatives)...")
    X, y, group = build_training_data(
        mentors_df,
        users_df,
        interactions_df,
        mentor_embeddings,
        mentor_quality_df,
        embedding_model,
        negatives_per_user=15,
        use_rating_as_label=True,
        random_state=42,
    )
    print(f"  Samples: {X.shape[0]}, groups: {len(group)}, features: {X.shape[1]}")

    print("Training LightGBM LambdaRank...")
    ltr_model = train_ltr(
        X, y, group,
        feature_names=LTR_FEATURE_NAMES,
        num_leaves=31,
        max_depth=6,
        n_estimators=150,
        learning_rate=0.05,
        min_data_in_leaf=20,
        random_state=42,
        verbose=10,
    )
    save_ltr_model(ltr_model, LTR_FEATURE_NAMES, models_dir)
    print(f"LTR model saved to {models_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
