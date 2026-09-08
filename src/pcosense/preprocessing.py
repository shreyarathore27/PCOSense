"""Reusable preprocessing for PCOSense models."""

from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def build_numeric_preprocessor(
    scale: bool = True,
) -> Pipeline:
    """Create preprocessing for numerical model features."""

    steps = [
        ("imputer", SimpleImputer(strategy="median")),
    ]

    if scale:
        steps.append(("scaler", StandardScaler()))

    return Pipeline(steps)

from sklearn.model_selection import train_test_split

from pcosense.features import TARGET_COLUMN


def create_train_test_split(
    data,
    features: list[str],
    test_size: float = 0.2,
    random_state: int = 42,
):
    """Create a stratified train/test split."""

    X = data[features].copy()
    y = data[TARGET_COLUMN].copy()

    return train_test_split(
        X,
        y,
        test_size=test_size,
        stratify=y,
        random_state=random_state,
    )