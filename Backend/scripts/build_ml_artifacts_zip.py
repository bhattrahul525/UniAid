"""
Build a zip of ML/models/ for upload to ML_ARTIFACTS_URL.
Run from Backend/:  python scripts/build_ml_artifacts_zip.py
Output: ML/models/ml-artifacts.zip (or path given as first arg). ML is at repo root.
"""
from pathlib import Path
import sys
import zipfile

BACKEND_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = BACKEND_ROOT.parent / "ML" / "models"
DEFAULT_ZIP = MODELS_DIR / "ml-artifacts.zip"


def main() -> None:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_ZIP
    if not MODELS_DIR.exists():
        print("ML models dir not found:", MODELS_DIR)
        print("Run first (from repo root): python ML/recommender.py build")
        sys.exit(1)
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in MODELS_DIR.iterdir():
            if f.is_file() and not f.name.startswith("."):
                zf.write(f, f.name)
    print("Created:", out)
    print("Upload this file and set ML_ARTIFACTS_URL to its URL.")


if __name__ == "__main__":
    main()
