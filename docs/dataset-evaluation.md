# Dataset evaluation (step 1)

**Decision:** use the Kottarathil Kaggle tabular set as the *primary* public dataset for PCOSense v1.

**Decision (how to use it):** treat it as a **clinic-labeled pattern dataset**, not as proof we can diagnose PCOS. Plan **two feature views** later (not implemented yet):

1. **Screening-style** — symptoms, cycle history, BMI/vitals, optional labs. **Exclude** follicle counts, follicle sizes, and endometrium thickness.
2. **Full clinical** — includes ultrasound. Use only as a comparison, because those features are often part of how the label is defined.

No model is trained in this step.

---

## 1. What we compared

Public PCOS *tabular* data is scarce. A 2025 survey of PCOS detection datasets ([Su et al., PMC12032871](https://pmc.ncbi.nlm.nih.gov/articles/PMC12032871/)) found that several “different” 541-row tables are **redistributions of the same Kerala cohort**. Image datasets exist but are out of scope until we have a tabular baseline.

| Candidate | What it is | Verdict |
| --- | --- | --- |
| **Kottarathil 2020 (Kaggle)** | ~541 women, ~40–45 clinical columns, 10 hospitals in Kerala, India. Target `PCOS (Y/N)`. Most cited numerical set (~40 papers in that survey). | **Use as primary.** Documented enough to audit leakage. |
| **Figshare “PCOS data.xlsx”** (Zafar et al., 320 rows, 160/160) | Genetics (DENND1A SNPs) plus clinical fields; used as “external validation” in some papers that then report **AUC = 1.0**. | **Do not use as the main set.** Different schema, genetics not in a future symptom app, perfect scores are a leakage/overfit warning. Optional later *schema-mapped* check only after we distrust 1.0 metrics. |
| **Kaggle ultrasound image dumps** | Follicle morphology CNNs. | Skip for v1. Different problem (vision), harder to explain to a beginner resume reader. |
| **UCI / NIH public tables** | No standard UCI “PCOS tabular” analogue to Pima diabetes. | None suitable. |
| **GitHub PCOS-Survey/PCOSData** | Small survey extract. | Too small / unclear protocol for a first ML project. |

There is **no large, multi-country, prospectively labeled, license-clear PCOS table** for open ML. That is a project constraint, not something we can paper over.

---

## 2. Primary dataset facts (from source + papers)

| Item | Detail |
| --- | --- |
| Source | [Kaggle: prasoonkottarathil/polycystic-ovary-syndrome-pcos](https://www.kaggle.com/datasets/prasoonkottarathil/polycystic-ovary-syndrome-pcos) |
| Collection | Clinical records from **10 hospitals, Kerala, India** (uploader description). Not a random population sample. |
| Size | Typically **541** rows. Papers report **~177 PCOS / ~364 non-PCOS** (about **33%** positive). Counts differ by 1–2 rows after dropping missing IDs. |
| Files | `PCOS_data_without_infertility.xlsx` (main) and `PCOS_infertility.csv` (subset / overlapping columns). Merge only after checking shared patient IDs; do not treat them as independent samples. |
| Label | `PCOS (Y/N)` as recorded in clinic files. **How Rotterdam/NIH criteria were applied is not published with the table.** |
| License | Confirm the badge **on the Kaggle page at download time**. A survey lists this cohort as **CC BY-NC-SA 4.0** in some mirrors; Kaggle copies sometimes say only “Data files © Original Authors”. **Assume non-commercial + attribution** until you read the live page. Do not commit the xlsx to GitHub. |
| Citation | Kottarathil, P. (2020). *Polycystic ovary syndrome (PCOS)*. Kaggle. |

### Feature inventory (names as used in papers; confirm after download)

Identifiers (drop from models): `Sl. No`, `Patient File No.`

**Demographics / body:** Age, Weight, Height, BMI, Blood Group, Hip, Waist, Waist:Hip Ratio

**Vitals:** Pulse rate, RR (breaths/min), BP systolic/diastolic, Hb

**Cycle / reproductive history:** Cycle (R/I), Cycle length (days), Marraige Status (Yrs) [sic], Pregnant (Y/N), No. of abortions

**Labs:** I beta-HCG, II beta-HCG, FSH, LH, FSH/LH, TSH, AMH, PRL, Vit D3, PRG, RBS

**Symptoms / lifestyle (mostly 0/1):** Weight gain, hair growth, Skin darkening, Hair loss, Pimples, Fast food, Reg.Exercise

**Ultrasound:** Follicle No. (L), Follicle No. (R), Avg. F size (L/R), Endometrium (mm)

Papers split these as roughly **24 non-invasive** vs **hormone + transvaginal ultrasound**.

---

## 3. Why this set is still the right *first* dataset

- It is the only widely reused **mixed clinical** table with a binary clinic label.
- Columns map onto a future app: cycle irregularity, BMI, hirsutism-like flags, optional labs.
- It is small enough to inspect **every column** (your step 2).
- It is large enough for a stratified train/test split, with the caveat that **n ≈ 540 is not a clinical trial**.

---

## 4. Methodological issues (must keep in the README)

### 4.1 Label leakage / circular diagnosis (highest risk)

PCOS is usually labeled with **Rotterdam-style rules**: two of three among (1) oligo/anovulation, (2) hyperandrogenism, (3) polycystic ovarian morphology (follicle count / ovarian volume).

If the Kaggle `PCOS (Y/N)` flag was assigned using follicle counts **and** irregular cycles **and** clinical hyperandrogenism (hair growth, acne), then a model that is given those same columns is mostly **re-learning the clinic’s rule**. That inflates accuracy and makes SHAP “discover” follicle number as #1 — which papers already report.

**What we will do later (not now):**

- Report metrics **with and without** ultrasound morphology features.
- Never treat 98–100% test accuracy as success.
- Do not call screening-style scores a “diagnosis”.

### 4.2 Selection bias

Rows are **hospital patients already being evaluated**, not people opening a wellness app. Dataset prevalence (~1 in 3) is **higher** than typical community PCOS prevalence (~8–13% depending on criteria and population). Precision/recall on this table **will not transfer** to a general user population without recalibration.

### 4.3 Geography and measurement

All sites are in **one Indian state**. Hormone assays, ultrasound machines, and symptom coding are not standardized in the public file. A Kerala-trained model is not “global PCOS risk”.

### 4.4 Derived columns and collinearity

- `BMI` is a function of weight and height.
- `FSH/LH` is a function of FSH and LH.
- `Waist:Hip Ratio` is a function of waist and hip.

Using parents **and** the ratio together does not add information; it can confuse coefficient-based models (logistic regression) and SHAP dependence plots.

### 4.5 Data quality red flags reported in published descriptives

These are reasons to **inspect raw values** in the next notebook, not to “fix” blindly:

| Signal | Why it matters |
| --- | --- |
| FSH max ~5052 mIU/mL, LH max ~2018, FSH/LH max ~1373 | Physiologically implausible; likely **decimal/unit typos**. A tree model can split on garbage and look accurate. |
| Pulse rate min **13** bpm | Almost certainly an entry error. |
| `Cycle length (days)` mean ≈ **5** | In English this sounds like inter-menstrual interval (~28 days). Here it is almost certainly **bleed duration**. Misreading this column invents a fake feature story. |
| `Cycle (R/I)` values **2 and 4** (not 0/1) | Encoding is not documented as a standard dummy. Must be mapped from the data, not assumed. |
| Missingness in marriage years, fast food, occasional AMH type issues | Papers impute median/mode **on the full dataset** — that is **test leakage**. Impute only inside the training fold later. |
| Unnamed extra Excel columns | Spreadsheet artifacts; drop after confirming they are empty. |

### 4.6 Class imbalance

~33% / 67% is **mild**, not extreme. Accuracy is still a bad headline metric because the majority class is “no PCOS”. We will compare Precision, Recall, F1, ROC-AUC, and the confusion matrix (your step 6). SMOTE in papers is often applied **before** the split — another leakage pattern we will not copy.

### 4.7 Identifiers

`Patient File No.` must never be a feature. If we ever merge the infertility file, we merge on ID and **deduplicate**.

### 4.8 “External validation” theater

Papers that train on Kaggle and then score 1.0 on Figshare (cyst size as a top feature) are not evidence of a production diagnostic. Perfect metrics on a second tiny table usually mean **the label is a function of the inputs** or the test set is not independent.

---

## 5. Assumptions we are making (questionable = flagged)

| Assumption | Status |
| --- | --- |
| The binary label is a consistent clinical PCOS assignment | **Unverified.** No codebook for criteria year or rater. |
| Yes/No symptom fields are comparable across 10 hospitals | **Questionable.** Self-report vs clinician exam is unknown. |
| Fast food / exercise are causal risk factors the model should use | **Lifestyle association only.** Easy to over-interpret in a UI. |
| AMH can stand in for ultrasound in a “non-invasive” model | **Research hypothesis**, not settled diagnostic replacement. |
| A future React form can collect the same features | **Only a subset.** Users will not enter FSH, follicle counts, or beta-HCG. That is why the screening feature view exists. |

---

## 6. What “validated” means here

We **did** validate:

- Public availability and reuse in peer-reviewed ML papers.
- Approximate size, label, geography, and column families.
- That this is the least-bad tabular option for an explainable beginner project.

We **did not** yet:

- Open the xlsx and count nulls ourselves (needs your Kaggle download).
- Confirm the live license badge.
- Prove the label-generation protocol.

That is the next increment: `notebooks/01_schema_and_quality.ipynb` after `python scripts/download_kaggle_pcos.py`.

---

## 7. Resume-safe wording (use later)

Good: “Built an explainable model of **clinic-labeled PCOS patterns** on a public Kerala cohort (n≈541), with a leakage audit (ultrasound vs symptom-only feature sets).”

Bad: “AI that diagnoses PCOS with 99% accuracy.”
