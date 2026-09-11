import json
from urllib.request import Request, urlopen

import pandas as pd

from pcosense.data import load_clean_data
from pcosense.features import FEATURE_SETS


df = load_clean_data()
features = FEATURE_SETS["screening"]

patient = {}

for feature in features:
    value = df.iloc[0][feature]

    if pd.isna(value):
        patient[feature] = None
    elif hasattr(value, "item"):
        patient[feature] = value.item()
    else:
        patient[feature] = value

payload = json.dumps({
    "patient_data": patient
}).encode("utf-8")

request = Request(
    "http://127.0.0.1:8000/predict",
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST",
)

with urlopen(request) as response:
    result = json.loads(response.read().decode("utf-8"))

print(json.dumps(result, indent=2))