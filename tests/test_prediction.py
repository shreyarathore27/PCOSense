import numpy as np
import pytest

from pcosense.predict import predict_pcos


class FakeModel:
    def predict_proba(self, patient_df):
        return np.array([[0.25, 0.75]])


def test_prediction_returns_expected_result(monkeypatch):
    fake_bundle = {
        "model": FakeModel(),
        "features": ["Age (yrs)", "BMI"],
        "threshold": 0.5,
        "model_name": "test_random_forest",
        "disclaimer": "Test disclaimer",
    }

    monkeypatch.setattr(
        "pcosense.predict.joblib.load",
        lambda path: fake_bundle
    )

    result = predict_pcos({
        "Age (yrs)": 25,
        "BMI": 24.5,
    })

    assert result["prediction"] == 1
    assert result["probability"] == 0.75
    assert result["label"] == "Higher screening likelihood"


def test_prediction_rejects_missing_features(monkeypatch):
    fake_bundle = {
        "model": FakeModel(),
        "features": ["Age (yrs)", "BMI"],
    }

    monkeypatch.setattr(
        "pcosense.predict.joblib.load",
        lambda path: fake_bundle
    )

    with pytest.raises(ValueError, match="BMI"):
        predict_pcos({"Age (yrs)": 25})