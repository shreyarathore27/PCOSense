"""Dataset loading and basic quality cleaning."""

from pathlib import Path

import numpy as np
import pandas as pd

from pcosense.config import RAW_DATA_DIR
from pcosense.features import validate_feature_sets

DATA_FILENAME = "PCOS_data_without_infertility.xlsx"
DATA_SHEET = "Full_new"


def load_raw_data(path: Path | None = None) -> pd.DataFrame:
    """Load the original PCOS Excel dataset."""

    data_path = path or RAW_DATA_DIR / DATA_FILENAME

    if not data_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {data_path}. "
            "Run scripts/download_kaggle_pcos.py first."
        )

    return pd.read_excel(data_path, sheet_name=DATA_SHEET)

def clean_base_data(data: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy without modifying the raw data."""

    cleaned = data.copy()

    cleaned.columns = (
        cleaned.columns
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

    artifact_columns = [
        column
        for column in cleaned.columns
        if column.startswith("Unnamed:")
    ]

    cleaned = cleaned.drop(columns=artifact_columns)

    for column in ["II beta-HCG(mIU/mL)", "AMH(ng/mL)"]:
        cleaned[column] = pd.to_numeric(
            cleaned[column],
            errors="coerce"
        )

    cleaned.loc[
        ~cleaned["Cycle(R/I)"].isin([2, 4]),
        "Cycle(R/I)"
    ] = np.nan

    cleaned.loc[
        cleaned["Cycle length(days)"] <= 0,
        "Cycle length(days)"
    ] = np.nan

    cleaned.loc[
        cleaned["Pulse rate(bpm)"] < 40,
        "Pulse rate(bpm)"
    ] = np.nan

    cleaned.loc[
        cleaned["BP _Systolic (mmHg)"] < 70,
        "BP _Systolic (mmHg)"
    ] = np.nan

    cleaned.loc[
        cleaned["BP _Diastolic (mmHg)"] < 40,
        "BP _Diastolic (mmHg)"
    ] = np.nan

    cleaned.loc[
        cleaned["FSH(mIU/mL)"] > 100,
        "FSH(mIU/mL)"
    ] = np.nan

    cleaned.loc[
        cleaned["LH(mIU/mL)"] > 100,
        "LH(mIU/mL)"
    ] = np.nan

    cleaned.loc[
        cleaned["Vit D3 (ng/mL)"] > 200,
        "Vit D3 (ng/mL)"
    ] = np.nan

    return cleaned

def load_clean_data(path: Path | None = None) -> pd.DataFrame:
    """Load, clean and validate the dataset."""

    cleaned = clean_base_data(load_raw_data(path))
    validate_feature_sets(cleaned.columns.tolist())

    return cleaned