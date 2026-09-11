from fastapi.testclient import TestClient

from pcosense.api import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_prediction_endpoint(monkeypatch):
    fake_result = {
        "prediction": 1,
        "label": "Higher screening likelihood",
        "probability": 0.75,
        "threshold": 0.5,
        "model_name": "test_model",
        "disclaimer": "Test disclaimer",
    }

    monkeypatch.setattr(
        "pcosense.api.predict_pcos",
        lambda patient_data: fake_result,
    )

    response = client.post(
        "/predict",
        json={"patient_data": {"Age (yrs)": 25}},
    )

    assert response.status_code == 200
    assert response.json() == fake_result


def test_prediction_endpoint_rejects_invalid_input(monkeypatch):
    def fake_prediction(patient_data):
        raise ValueError("Missing required features: ['BMI']")

    monkeypatch.setattr(
        "pcosense.api.predict_pcos",
        fake_prediction,
    )

    response = client.post(
        "/predict",
        json={"patient_data": {"Age (yrs)": 25}},
    )

    assert response.status_code == 422
    assert "BMI" in response.json()["detail"]