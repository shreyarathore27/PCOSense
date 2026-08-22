"""Download the chosen public dataset into data/raw/. No cleaning or modeling."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from pcosense.config import KAGGLE_DATASET, RAW_DATA_DIR


def download_kaggle_pcos(dest: Path | None = None) -> Path:
    """Copy Kaggle files into data/raw/ using kagglehub.

    Requires a Kaggle account and local credentials (kaggle.json).
    This script only downloads; it does not train models or rewrite labels.
    """
    try:
        import kagglehub
    except ImportError as exc:
        raise SystemExit(
            "kagglehub is not installed. From the project root run:\n"
            "  python -m venv .venv\n"
            "  .venv\\Scripts\\activate\n"
            "  pip install -r requirements.txt"
        ) from exc

    dest = dest or RAW_DATA_DIR
    dest.mkdir(parents=True, exist_ok=True)

    cached = Path(kagglehub.dataset_download(KAGGLE_DATASET))
    copied: list[str] = []
    for src in cached.rglob("*"):
        if src.is_file():
            target = dest / src.name
            shutil.copy2(src, target)
            copied.append(src.name)

    if not copied:
        raise SystemExit(f"Download succeeded but no files were found under {cached}")

    print(f"Cached at: {cached}")
    print(f"Copied {len(copied)} file(s) to: {dest}")
    for name in sorted(copied):
        print(f"  - {name}")
    return dest


def main() -> None:
    parser = argparse.ArgumentParser(description="Download the Kaggle PCOS tabular dataset.")
    parser.parse_args()
    download_kaggle_pcos()


if __name__ == "__main__":
    main()
