import os
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from pcosense.predict import load_model_bundle, predict_pcos


app = FastAPI(
    title="PCOSense API",
    description="Educational PCOS screening API",
    version="1.0.0",
)

frontend_urls = os.getenv(
    "FRONTEND_URLS",
    "http://localhost:3000,http://localhost:5173",
)

allowed_origins = [
    url.strip().rstrip("/")
    for url in frontend_urls.split(",")
    if url.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PredictionRequest(BaseModel):
    patient_data: dict[str, Any]


@app.get("/")
def root():
    return {
        "name": "PCOSense API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/model-info")
def model_info():
    try:
        bundle = load_model_bundle()

        return {
            "model_name": bundle["model_name"],
            "feature_set": bundle["feature_set"],
            "feature_count": len(bundle["features"]),
            "features": bundle["features"],
            "threshold": bundle["threshold"],
            "disclaimer": bundle["disclaimer"],
        }
    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="Model file not found. Run the training script first.",
        )


@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        return predict_pcos(request.patient_data)

    except ValueError as error:
        raise HTTPException(
            status_code=422,
            detail=str(error),
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=503,
            detail="Model file not found. Run the training script first.",
        )