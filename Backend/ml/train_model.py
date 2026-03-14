"""
Training entrypoint for the recommendation model.

The current recommendation engine is rule-based (similarity on field, country,
language, experience), so there is no trainable model to persist. This script
is a placeholder for future ML training (e.g. learning weights or training
a classifier). Run from project root:

    python -m ml.train_model
"""
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train() -> None:
    """Placeholder: no trainable model in the current rule-based setup."""
    logger.info("Recommendation model is rule-based; no training step required.")
    logger.info("To add ML training, implement weight learning or model fitting here.")


if __name__ == "__main__":
    train()
