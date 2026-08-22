# Data directory

Patient-level records are **not committed**. Download locally after reading `docs/dataset-evaluation.md`.

| Folder | Role |
| --- | --- |
| `raw/` | Unchanged files from the source (xlsx/csv). |
| `interim/` | Cleaning experiments (later). |
| `processed/` | Train/test splits and model-ready tables (later). |

## Download (after creating a free Kaggle account)

1. Create an API token at [Kaggle account settings](https://www.kaggle.com/settings) (`kaggle.json`).
2. Place it at `%USERPROFILE%\.kaggle\kaggle.json` (Windows).
3. From the project root, with the virtualenv active:

```powershell
pip install -e .
python scripts/download_kaggle_pcos.py
```

Expected files (Kaggle v3):

- `PCOS_data_without_infertility.xlsx` — main table (~541 rows).
- `PCOS_infertility.csv` — overlapping infertility-related columns; **not** a second independent cohort.

Cite the uploader in any README, paper, or resume bullet:

> Kottarathil, P. (2020). Polycystic ovary syndrome (PCOS). Kaggle.  
> https://www.kaggle.com/datasets/prasoonkottarathil/polycystic-ovary-syndrome-pcos
