from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

from pcosense.data import load_clean_data
from pcosense.features import FEATURE_SETS
from pcosense.preprocessing import build_numeric_preprocessor


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODEL_DIR / "pcos_screening_model.joblib"


def train_final_model():
    df = load_clean_data()

    features = FEATURE_SETS["screening"]
    X = df[features]
    y = df["PCOS (Y/N)"]

    pipeline = Pipeline([
        ("preprocessor", build_numeric_preprocessor()),
        ("model", RandomForestClassifier(
            n_estimators=700,
            min_samples_split=5,
            min_samples_leaf=3,
            max_features="log2",
            max_depth=6,
            class_weight="balanced_subsample",
            random_state=42,
            n_jobs=-1
        ))
    ])

    # Final model uses all available data after evaluation is complete.
    pipeline.fit(X, y)

    model_bundle = {
        "model": pipeline,
        "features": features,
        "feature_set": "screening",
        "threshold": 0.5,
        "model_name": "tuned_random_forest",
        "disclaimer": "For educational screening only, not medical diagnosis."
    }

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model_bundle, MODEL_PATH)

    print(f"Final model trained on {len(X)} records")
    print(f"Number of features: {len(features)}")
    print(f"Saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_final_model()