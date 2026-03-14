"""
Learning-to-rank (LTR) for mentor recommendation.

Trains a LightGBM LambdaRank model on (mentee, mentor) pairs from interactions,
using semantic similarity, quality signals, and explicit match features.
At inference, candidates are scored by the LTR model for optimal ranking.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

# Feature names in fixed order (train and inference must match)
LTR_FEATURE_NAMES = [
    "similarity",
    "quality_score",
    "past_interaction",
    "university_match",
    "field_cs_match",
    "visa_match",
    "housing_match",
    "cultural_match",
    "career_match",
    "language_match",
    "mentor_rating_norm",
    "success_rate",
    "interaction_count_norm",
    "availability_norm",
    "response_time_inv",
]

# Language names we detect in request text (lowercase)
_LANGUAGE_KEYWORDS = (
    "mandarin", "chinese", "english", "spanish", "french", "hindi", "arabic",
    "italian", "german", "japanese", "korean", "vietnamese", "thai", "indonesian",
    "malay", "portuguese", "russian", "bengali", "tamil", "telugu", "turkish",
)


def _safe_float(x: Any, default: float = 0.0) -> float:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return default
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def _safe_str(x: Any) -> str:
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return ""
    return str(x).strip().lower()


def _field_cs_match(field: Any) -> float:
    """1.0 if mentor field is CS/tech related."""
    s = _safe_str(field)
    if not s:
        return 0.0
    keywords = (
        "computer", "computing", "data science", "software", "programming",
        "information technology", "it ", " cs ", "cs", "informatics",
    )
    return 1.0 if any(k in s for k in keywords) else 0.0


def _university_match(mentor_uni: Any, query_uni: Optional[str]) -> float:
    """1.0 if mentor university matches the requested/target university."""
    if not query_uni or not str(query_uni).strip():
        return 0.0
    return 1.0 if _safe_str(mentor_uni) == _safe_str(query_uni) else 0.0


def _detect_requested_languages(request_text: Optional[str]) -> List[str]:
    """Detect which languages are mentioned in request text."""
    if not request_text or not str(request_text).strip():
        return []
    t = _safe_str(request_text)
    return [lang for lang in _LANGUAGE_KEYWORDS if lang in t]


def _mentor_speaks_any(mentor: Dict[str, Any], languages: List[str]) -> bool:
    """True if mentor's languages_spoken contains any of the requested languages."""
    if not languages:
        return True
    spoken = (mentor.get("languages_spoken") or "").strip()
    if not spoken:
        return False
    parts = [p.strip().lower() for p in spoken.replace(";", ",").split(",") if p.strip()]
    for req in languages:
        for part in parts:
            if req in part or part in req:
                return True
    return False


def _request_mentor_match(
    mentor: Dict[str, Any],
    request_text: Optional[str],
    university_from_query: Optional[str],
) -> Tuple[float, float, float, float, float, float, float]:
    """
    From request_text and optional university, compute explicit match flags
    (university_match, field_cs_match, visa_match, housing_match, cultural_match, career_match).
    Returns (university_match, field_cs_match, visa_match, housing_match, cultural_match, career_match).
    """
    t = (_safe_str(request_text) or "") if request_text else ""
    uni_match = _university_match(mentor.get("university"), university_from_query)

    field_match = 0.0
    if any(k in t for k in ("computer", "computing", "data science", "software", " cs ", "cs ", " it ", "information technology")):
        field_match = _field_cs_match(mentor.get("field_of_study"))

    visa = 1.0 if (any(k in t for k in ("visa", "immigration")) and _safe_float(mentor.get("visa_experience")) == 1.0) else 0.0
    housing = 1.0 if (any(k in t for k in ("housing", "accommodation")) and _safe_float(mentor.get("housing_experience")) == 1.0) else 0.0
    cultural = 1.0 if (any(k in t for k in ("cultural", "culture", "adaptation")) and _safe_float(mentor.get("cultural_adaptation_experience")) == 1.0) else 0.0
    career = 1.0 if (any(k in t for k in ("career", "job", "employment")) and _safe_float(mentor.get("career_guidance_experience")) == 1.0) else 0.0
    requested_languages = _detect_requested_languages(request_text)
    language_match = 1.0 if requested_languages and _mentor_speaks_any(mentor, requested_languages) else 0.0

    return uni_match, field_match, visa, housing, cultural, career, language_match


def _profile_mentor_match(
    mentor: Dict[str, Any],
    user_profile: Optional[Dict[str, Any]],
    university_from_query: Optional[str],
) -> Tuple[float, float, float, float, float, float, float]:
    """
    From user profile (mentee) and optional university, compute explicit match flags.
    Returns (university_match, field_cs_match, visa_match, housing_match, cultural_match, career_match, language_match).
    """
    uni = university_from_query or (user_profile.get("target_university") if user_profile else None)
    uni_match = _university_match(mentor.get("university"), uni)

    field_match = 0.0
    if user_profile and _safe_float(user_profile.get("concern_academics")) == 1.0:
        field_match = _field_cs_match(mentor.get("field_of_study"))
    if user_profile and _field_cs_match(user_profile.get("field_of_study")) == 1.0:
        field_match = max(field_match, _field_cs_match(mentor.get("field_of_study")))

    visa = 1.0 if (user_profile and _safe_float(user_profile.get("concern_visa")) == 1.0 and _safe_float(mentor.get("visa_experience")) == 1.0) else 0.0
    housing = 1.0 if (user_profile and _safe_float(user_profile.get("concern_accommodation")) == 1.0 and _safe_float(mentor.get("housing_experience")) == 1.0) else 0.0
    cultural = 1.0 if (user_profile and _safe_float(user_profile.get("concern_culture")) == 1.0 and _safe_float(mentor.get("cultural_adaptation_experience")) == 1.0) else 0.0
    career = 1.0 if (user_profile and _safe_float(user_profile.get("concern_career")) == 1.0 and _safe_float(mentor.get("career_guidance_experience")) == 1.0) else 0.0
    pref_lang = (user_profile.get("preferred_language") or "").strip().lower() if user_profile else ""
    if pref_lang:
        language_match = 1.0 if _mentor_speaks_any(mentor, [pref_lang]) else 0.0
    else:
        language_match = 0.0

    return uni_match, field_match, visa, housing, cultural, career, language_match


def build_ltr_features_row(
    *,
    similarity: float,
    quality_score: float,
    past_interaction: float,
    mentor: Dict[str, Any],
    mentor_quality: Dict[str, Any],
    request_text: Optional[str] = None,
    user_profile: Optional[Dict[str, Any]] = None,
    university_from_query: Optional[str] = None,
    rating_max: float = 5.0,
    interaction_count_max: float = 1.0,
    availability_max: float = 1.0,
    response_time_max: float = 1.0,
) -> List[float]:
    """
    Build one row of LTR features for a single (query, mentor) pair.
    Used at inference. For training, use build_ltr_features_df.
    """
    if request_text:
        uni_match, field_match, visa, housing, cultural, career, language_match = _request_mentor_match(
            mentor, request_text, university_from_query
        )
    else:
        uni_match, field_match, visa, housing, cultural, career, language_match = _profile_mentor_match(
            mentor, user_profile, university_from_query
        )

    mentor_rating = _safe_float(mentor.get("mentor_rating"), 0.0)
    mentor_rating_norm = mentor_rating / rating_max if rating_max > 0 else 0.0

    success_rate = _safe_float(mentor_quality.get("success_rate"), 0.0)
    interaction_count = _safe_float(mentor_quality.get("interaction_count"), 0.0)
    interaction_count_norm = min(1.0, interaction_count / interaction_count_max) if interaction_count_max > 0 else 0.0

    availability = _safe_float(mentor.get("availability_hours_per_week"), 0.0)
    availability_norm = min(1.0, availability / availability_max) if availability_max > 0 else 0.0

    response_time = _safe_float(mentor.get("response_time_hours"), 48.0)
    response_time_inv = 1.0 / (1.0 + response_time) if response_time >= 0 else 0.0
    if response_time_max > 0:
        response_time_inv = response_time_inv / (1.0 / (1.0 + response_time_max))

    return [
        similarity,
        quality_score,
        past_interaction,
        uni_match,
        field_match,
        visa,
        housing,
        cultural,
        career,
        language_match,
        mentor_rating_norm,
        success_rate,
        interaction_count_norm,
        availability_norm,
        response_time_inv,
    ]


def build_ltr_features_df(
    candidates_df: pd.DataFrame,
    request_text: Optional[str] = None,
    user_profile: Optional[Dict[str, Any]] = None,
    university_from_query: Optional[str] = None,
    *,
    mentor_quality_df: pd.DataFrame,
    rating_max: Optional[float] = None,
    interaction_count_max: Optional[float] = None,
    availability_max: Optional[float] = None,
) -> pd.DataFrame:
    """
    Build LTR feature matrix for a candidates DataFrame (e.g. from recommender).
    candidates_df must have: mentor_id, similarity, quality_score, past_interaction,
    and mentor columns (university, field_of_study, visa_experience, etc.).
    mentor_quality_df must have mentor_id, success_rate, interaction_count.
    """
    quality_by_id = mentor_quality_df.set_index("mentor_id").to_dict(orient="index")
    if rating_max is None:
        rating_max = max(1.0, candidates_df["mentor_rating"].max() if "mentor_rating" in candidates_df.columns else 5.0)
    if interaction_count_max is None:
        interaction_count_max = max(1.0, mentor_quality_df["interaction_count"].max() if "interaction_count" in mentor_quality_df.columns else 1.0)
    if availability_max is None:
        availability_max = max(1.0, candidates_df["availability_hours_per_week"].max() if "availability_hours_per_week" in candidates_df.columns else 1.0)
    response_time_max = 72.0

    rows = []
    for _, row in candidates_df.iterrows():
        mentor = row.to_dict()
        mid = int(row.get("mentor_id", 0))
        mentor_quality = quality_by_id.get(mid, {})
        if not isinstance(mentor_quality, dict):
            mentor_quality = {}
        feat = build_ltr_features_row(
            similarity=float(row.get("similarity", 0.0)),
            quality_score=float(row.get("quality_score", 0.0)),
            past_interaction=float(row.get("past_interaction", 0.0)),
            mentor=mentor,
            mentor_quality=mentor_quality,
            request_text=request_text,
            user_profile=user_profile,
            university_from_query=university_from_query,
            rating_max=rating_max,
            interaction_count_max=interaction_count_max,
            availability_max=availability_max,
            response_time_max=response_time_max,
        )
        rows.append(feat)

    return pd.DataFrame(rows, columns=LTR_FEATURE_NAMES)


def train_ltr(
    X: np.ndarray,
    y: np.ndarray,
    group: np.ndarray,
    feature_names: List[str],
    *,
    num_leaves: int = 31,
    max_depth: int = 6,
    n_estimators: int = 100,
    learning_rate: float = 0.05,
    min_data_in_leaf: int = 20,
    random_state: int = 42,
    verbose: int = 0,
) -> Any:
    """
    Train a LightGBM LambdaRank model.
    X: (n_samples, n_features), y: relevance labels (e.g. 0/1 or 1-5), group: sizes of each query group.
    """
    try:
        import lightgbm as lgb
    except ImportError:
        raise ImportError("lightgbm is required for LTR. Install with: pip install lightgbm")

    # Lambdarank expects integer relevance labels; use label_gain for graded relevance
    y_int = np.asarray(y, dtype=np.int32)
    if np.issubdtype(y.dtype, np.floating) and not np.issubdtype(y.dtype, np.integer):
        # Bin float [0,1] into 0-5 for NDCG-style gains
        y_int = np.clip(np.round(y * 5).astype(np.int32), 0, 5)
    train_data = lgb.Dataset(X, label=y_int, group=group, feature_name=feature_names)
    # Gains for relevance 0..5 (higher = better)
    label_gain = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    params = {
        "objective": "lambdarank",
        "metric": "ndcg",
        "ndcg_eval_at": [1, 3, 5, 10],
        "label_gain": label_gain,
        "num_leaves": num_leaves,
        "max_depth": max_depth,
        "learning_rate": learning_rate,
        "min_data_in_leaf": min_data_in_leaf,
        "verbosity": -1,
        "random_state": random_state,
        "force_col_wise": True,
    }
    model = lgb.train(
        params,
        train_data,
        num_boost_round=n_estimators,
        valid_sets=[train_data],
        callbacks=[lgb.log_evaluation(period=verbose)],
    )
    return model


def save_ltr_model(model: Any, feature_names: List[str], path_dir: Path) -> None:
    """Save LightGBM model and feature names to path_dir."""
    path_dir = Path(path_dir)
    path_dir.mkdir(parents=True, exist_ok=True)
    model.save_model(str(path_dir / "ltr_model.txt"))
    with open(path_dir / "ltr_features.json", "w") as f:
        json.dump(feature_names, f, indent=2)


def load_ltr_model(path_dir: Path) -> Tuple[Any, List[str]]:
    """Load LightGBM model and feature names from path_dir. Returns (model, feature_names)."""
    try:
        import lightgbm as lgb
    except ImportError:
        raise ImportError("lightgbm is required for LTR. Install with: pip install lightgbm")

    path_dir = Path(path_dir)
    model = lgb.Booster(model_file=str(path_dir / "ltr_model.txt"))
    with open(path_dir / "ltr_features.json") as f:
        feature_names = json.load(f)
    return model, feature_names


def score_with_ltr(model: Any, X: pd.DataFrame, feature_names: List[str]) -> np.ndarray:
    """Score candidates with the LTR model. X must have columns matching feature_names."""
    for name in feature_names:
        if name not in X.columns:
            raise ValueError(f"LTR feature missing: {name}")
    X = X[feature_names]
    return model.predict(X)
