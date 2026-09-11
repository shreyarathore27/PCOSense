from pathlib import Path
from typing import Any, Mapping

import joblib
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MODEL_PATH = PROJECT_ROOT / "models" / "pcos_screening_model.joblib"


def load_model_bundle(model_path: Path | str = DEFAULT_MODEL_PATH):
    """Load the saved PCOS screening model bundle."""
    return joblib.load(Path(model_path))


def predict_pcos(
    patient_data: Mapping[str, Any],
    model_path: Path | str = DEFAULT_MODEL_PATH,
) -> dict:
    """Generate a PCOS screening prediction for one patient."""

    bundle = load_model_bundle(model_path)
    features = bundle["features"]

    missing_features = [
        feature for feature in features
        if feature not in patient_data
    ]

    if missing_features:
        raise ValueError(
            f"Missing required features: {missing_features}"
        )

    patient_df = pd.DataFrame([{
        feature: patient_data[feature]
        for feature in features
    }])

    probability = float(
        bundle["model"].predict_proba(patient_df)[0, 1]
    )

    threshold = float(bundle.get("threshold", 0.5))
    prediction = int(probability >= threshold)

    return {
        "prediction": prediction,
        "label": "Higher screening likelihood" if prediction else "Lower screening likelihood",
        "probability": round(probability, 4),
        "threshold": threshold,
        "model_name": bundle.get("model_name", "unknown"),
        "disclaimer": bundle.get(
            "disclaimer",
            "For educational screening only, not medical diagnosis."
        ),
    }