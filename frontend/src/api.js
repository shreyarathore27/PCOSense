const API_URL =
  import.meta.env.VITE_API_URL ||
  "http://127.0.0.1:8000";
export async function getModelInfo() {
  const response = await fetch(`${API_URL}/model-info`);

  if (!response.ok) {
    throw new Error("Could not connect to the PCOSense backend.");
  }

  return response.json();
}

export async function requestPrediction(patientData) {
  const response = await fetch(`${API_URL}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      patient_data: patientData,
    }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Prediction failed.");
  }

  return data;
}