# PCOSense

Explainable machine learning for **PCOS pattern / risk assessment**.

 It is **not** a diagnostic tool, medical device, or substitute for clinical care. See `docs/project-scope.md`.

## Current status

**Step 1 (this commit):** repository layout + evaluation of a public dataset.  
**Not started:** EDA, preprocessing, models, SHAP, API, UI.

## Why this dataset

We will use the public Kaggle table compiled by Prasoon Kottarathil (Kerala hospital records, n≈541). It is the standard open **tabular** PCOS set in ML papers. It is also easy to misuse: ultrasound follicle counts often dominate models because they are close to how PCOS is *defined*.

Full audit, license notes, and rejected alternatives: [`docs/dataset-evaluation.md`](docs/dataset-evaluation.md).

## Layout

```
PCOSense/
  docs/                 Design notes (start here)
  data/                 Local data only; not committed
  notebooks/            One question per notebook
  src/pcosense/         Shared Python (paths, later pipelines)
  scripts/              Download / ops helpers
  reports/figures/      Saved plots (later)
  models/               Saved estimators (later)
```

Backend (`FastAPI`) and frontend (`React`) are **intentionally omitted** until the ML core is honest and documented.

## Setup (Windows / PowerShell)

Python 3.11+ recommended.

```powershell
cd $env:USERPROFILE\PCOSense
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -e .
```

Download the dataset (Kaggle account + `kaggle.json` required):

```powershell
python scripts\download_kaggle_pcos.py
```

## Roadmap

1. Dataset choice and project structure — **this step**
2. EDA, column-by-column
3. Preprocessing + feature engineering
4. Leakage-free split + class imbalance handling
5. Logistic Regression, Random Forest, XGBoost
6. Precision / Recall / F1 / ROC-AUC / confusion matrix
7. SHAP (global + per-person)
8. FastAPI
9. React
10. Cycle/symptom tracking + anomaly detection
11. Deploy and GitHub polish

## Citation (dataset)

Kottarathil, P. (2020). Polycystic ovary syndrome (PCOS). Kaggle.  
https://www.kaggle.com/datasets/prasoonkottarathil/polycystic-ovary-syndrome-pcos
