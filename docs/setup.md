# PCOSense Local Setup

## Prerequisites

Install:

- Python 3.12
- Node.js 20.19+ or 22.12+
- Git
- A Kaggle account

## 1. Clone the repository

```powershell
git clone https://github.com/shreyarathore27/PCOSense.git
cd PCOSense
```

## 2. Create the Python environment

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

## 3. Install Python dependencies

```powershell
pip install -r requirements.txt
pip install -e .
```

## 4. Configure Kaggle

Download your Kaggle API token and save it as:

```text
C:\Users\<your-username>\.kaggle\kaggle.json
```

Never commit `kaggle.json` to GitHub.

## 5. Download the dataset

```powershell
python scripts\download_kaggle_pcos.py
```

The dataset will be placed in:

```text
data/raw/
```

## 6. Train the final model

```powershell
python scripts\train_final_model.py
```

This creates:

```text
models/pcos_screening_model.joblib
```

The generated model is not stored in Git.

## 7. Run backend tests

```powershell
python -m pytest -v
```

## 8. Start the FastAPI backend

```powershell
python -m uvicorn pcosense.api:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

## 9. Start the React frontend

Open a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

## 10. Check the frontend

```powershell
npm run lint
npm run build
```

## Disclaimer

PCOSense is an educational machine-learning project. It does not provide medical diagnosis or treatment guidance.