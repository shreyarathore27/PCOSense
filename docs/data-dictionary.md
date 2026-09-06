# PCOSense Data Dictionary


This document describes the columns in the primary PCOS dataset used by PCOSense.

- One row represents one patient record.
- Target column: `PCOS (Y/N)`
- Original records: 541
- Original columns: 45
- `Unnamed: 44` is an Excel artifact and is excluded.

## Column inventory

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path.cwd()

if PROJECT_ROOT.name == "notebooks":
    PROJECT_ROOT = PROJECT_ROOT.parent

DATA_PATH = PROJECT_ROOT / "data" / "raw" / "PCOS_data_without_infertility.xlsx"

df = pd.read_excel(DATA_PATH)

print("Dataset shape:", df.shape)
df.head()
print("Columns:")
for number, column in enumerate(df.columns, start=1):
    print(f"{number}. {column}")

print("\nData types:")
df.info()
missing_values = df.isnull().sum()
missing_values = missing_values[missing_values > 0].sort_values(ascending=False)

print("Missing values:")
display(missing_values)

print("Duplicate rows:", df.duplicated().sum())

if "Patient File No." in df.columns:
    print(
        "Duplicate patient IDs:",
        df["Patient File No."].duplicated().sum()
    )
excel_file = pd.ExcelFile(DATA_PATH)

print("Sheet names:", excel_file.sheet_names)

for sheet in excel_file.sheet_names:
    sheet_df = pd.read_excel(DATA_PATH, sheet_name=sheet)
    print(sheet, sheet_df.shape)
df = pd.read_excel(
    DATA_PATH,
    sheet_name="Full_new"
)

print("Dataset shape:", df.shape)
df.head()
empty_columns = [
    column for column in df.columns
    if df[column].isna().all()
]

print("Completely empty columns:", empty_columns)
df_clean = df.drop(columns=empty_columns).copy()

print("Original shape:", df.shape)
print("Working shape:", df_clean.shape)
print("Target counts:")
display(df_clean["PCOS (Y/N)"].value_counts(dropna=False))

print("Target percentages:")
display(
    df_clean["PCOS (Y/N)"]
    .value_counts(normalize=True, dropna=False)
    .mul(100)
    .round(2)
)

print("Duplicate rows:", df_clean.duplicated().sum())
print(
    "Duplicate patient IDs:",
    df_clean["Patient File No."].duplicated().sum()
)
missing_report = pd.DataFrame({
    "missing_count": df_clean.isna().sum(),
    "missing_percent": (
        df_clean.isna().mean() * 100
    ).round(2)
})

missing_report = missing_report[
    missing_report["missing_count"] > 0
].sort_values("missing_count", ascending=False)

display(missing_report)
display(
    df.loc[
        df["Unnamed: 44"].notna(),
        ["Patient File No.", "Unnamed: 44"]
    ]
)
display(
    df.loc[
        df["Marraige Status (Yrs)"].isna()
        | df["Fast food (Y/N)"].isna(),
        [
            "Patient File No.",
            "Marraige Status (Yrs)",
            "Fast food (Y/N)",
            "PCOS (Y/N)"
        ]
    ]
)
column_report = pd.DataFrame({
    "column": df.columns,
    "data_type": df.dtypes.astype(str).values,
    "unique_values": df.nunique(dropna=True).values
})

display(column_report)
clean_df = df.drop(columns=["Unnamed: 44"]).copy()

print("Original shape:", df.shape)
print("Working shape:", clean_df.shape)
for column in clean_df.columns:
    if "HCG" in column.upper() or "AMH" in column.upper():
        print(repr(column))
clean_df.columns = (
    clean_df.columns
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

print("Column names cleaned.")
for column in clean_df.columns:
    if "HCG" in column.upper() or "AMH" in column.upper():
        print(repr(column))
for column in ["II beta-HCG(mIU/mL)", "AMH(ng/mL)"]:
    converted = pd.to_numeric(clean_df[column], errors="coerce")

    invalid = clean_df.loc[
        converted.isna() & clean_df[column].notna(),
        ["Patient File No.", column]
    ]

    print(f"\nInvalid values in {column}:")
    display(invalid)
for column in [
    "Cycle(R/I)",
    "BP _Systolic (mmHg)",
    "BP _Diastolic (mmHg)"
]:
    print(f"\n{column}:")
    display(clean_df[column].value_counts(dropna=False).sort_index())
columns_to_describe = [
    "Age (yrs)",
    "Pulse rate(bpm)",
    "Cycle length(days)",
    "FSH(mIU/mL)",
    "LH(mIU/mL)",
    "FSH/LH",
    "TSH (mIU/L)",
    "Vit D3 (ng/mL)"
]

display(
    clean_df[columns_to_describe]
    .describe()
    .T[["min", "mean", "50%", "max"]]
)
suspicious_mask = (
    (clean_df["Pulse rate(bpm)"] < 40)
    | (clean_df["Cycle length(days)"] < 1)
    | (clean_df["Cycle(R/I)"] == 5)
    | (clean_df["BP _Systolic (mmHg)"] < 70)
    | (clean_df["BP _Diastolic (mmHg)"] < 40)
    | (clean_df["FSH(mIU/mL)"] > 100)
    | (clean_df["LH(mIU/mL)"] > 100)
    | (clean_df["TSH (mIU/L)"] > 20)
    | (clean_df["Vit D3 (ng/mL)"] > 200)
)

display(clean_df.loc[suspicious_mask])
target_counts = clean_df["PCOS (Y/N)"].value_counts().sort_index()
target_percentages = (
    clean_df["PCOS (Y/N)"]
    .value_counts(normalize=True)
    .sort_index()
    .mul(100)
    .round(2)
)

display(pd.DataFrame({
    "count": target_counts,
    "percentage": target_percentages
}))
print(
    "IDs contain identical values:",
    clean_df["Sl. No"].equals(clean_df["Patient File No."])
)

print("Duplicate Sl. No:", clean_df["Sl. No"].duplicated().sum())
print(
    "Duplicate Patient File No.:",
    clean_df["Patient File No."].duplicated().sum()
)
calculated_bmi = clean_df["Weight (Kg)"] / (
    clean_df["Height(Cm)"] / 100
) ** 2

calculated_fsh_lh = (
    clean_df["FSH(mIU/mL)"] / clean_df["LH(mIU/mL)"]
)

calculated_waist_hip = (
    clean_df["Waist(inch)"] / clean_df["Hip(inch)"]
)

print("Largest BMI difference:", (clean_df["BMI"] - calculated_bmi).abs().max())
print("Largest FSH/LH difference:", (clean_df["FSH/LH"] - calculated_fsh_lh).abs().max())
print(
    "Largest Waist:Hip difference:",
    (clean_df["Waist:Hip Ratio"] - calculated_waist_hip).abs().max()
)
checks = {
    "Very low pulse": ("Pulse rate(bpm)", clean_df["Pulse rate(bpm)"] < 40),
    "Cycle length below 1": ("Cycle length(days)", clean_df["Cycle length(days)"] < 1),
    "Unexpected cycle code": ("Cycle(R/I)", clean_df["Cycle(R/I)"] == 5),
    "Very low systolic BP": ("BP _Systolic (mmHg)", clean_df["BP _Systolic (mmHg)"] < 70),
    "Very low diastolic BP": ("BP _Diastolic (mmHg)", clean_df["BP _Diastolic (mmHg)"] < 40),
    "FSH above 100": ("FSH(mIU/mL)", clean_df["FSH(mIU/mL)"] > 100),
    "LH above 100": ("LH(mIU/mL)", clean_df["LH(mIU/mL)"] > 100),
    "TSH above 20": ("TSH (mIU/L)", clean_df["TSH (mIU/L)"] > 20),
    "Vitamin D3 above 200": ("Vit D3 (ng/mL)", clean_df["Vit D3 (ng/mL)"] > 200),
}

issues = []

for issue, (column, mask) in checks.items():
    for _, row in clean_df.loc[mask, ["Patient File No.", column]].iterrows():
        issues.append({
            "Patient File No.": row["Patient File No."],
            "issue": issue,
            "column": column,
            "value": row[column]
        })

issues_df = pd.DataFrame(issues)
display(issues_df.sort_values("Patient File No."))
bmi_check = clean_df[
    ["Patient File No.", "Weight (Kg)", "Height(Cm)", "BMI"]
].copy()

bmi_check["Calculated BMI"] = calculated_bmi
bmi_check["Difference"] = (
    bmi_check["BMI"] - bmi_check["Calculated BMI"]
).abs()

display(bmi_check.sort_values("Difference", ascending=False).head(10))
quality_summary = pd.DataFrame({
    "issue": [
        "Missing marriage status",
        "Missing fast-food value",
        "Invalid II beta-HCG",
        "Invalid AMH"
    ],
    "count": [1, 1, 1, 1]
})

display(quality_summary)
## Initial audit findings

- Dataset contains 541 records and 45 original columns.
- `Unnamed: 44` is a spreadsheet artifact and should be removed.
- `Sl. No` and `Patient File No.` contain identical unique identifiers.
- Target distribution: 364 non-PCOS and 177 PCOS records.
- One value is missing from `Marraige Status (Yrs)`.
- One value is missing from `Fast food (Y/N)`.
- `II beta-HCG(mIU/mL)` contains the invalid value `1.99.`
- `AMH(ng/mL)` contains the invalid value `a`.
- Suspected data-entry errors exist in pulse, blood pressure, cycle encoding, FSH, LH and Vitamin D3.
- Some stored BMI values differ from BMI recalculated using weight and height.
- No values have been corrected or imputed during this audit.
dictionary_df = pd.DataFrame({
    "Column": clean_df.columns,
    "Data type": clean_df.dtypes.astype(str).values,
    "Unique values": clean_df.nunique(dropna=True).values,
    "Missing values": clean_df.isna().sum().values
})

header = "| Column | Data type | Unique values | Missing values |"
separator = "|---|---|---:|---:|"

rows = [
    f"| `{row['Column']}` | {row['Data type']} | "
    f"{row['Unique values']} | {row['Missing values']} |"
    for _, row in dictionary_df.iterrows()
]

markdown_table = "\n".join([header, separator] + rows)
print(markdown_table)

## Column groups

### Identifiers — exclude from models

- `Sl. No`
- `Patient File No.`

Both contain the same sequential patient identifiers.

### Prediction target

- `PCOS (Y/N)` — clinic-recorded binary label:
  - `0`: PCOS-negative
  - `1`: PCOS-positive

### Demographics and body measurements

- Age, weight, height and BMI
- Blood group
- Hip and waist measurements
- Waist-to-hip ratio

### Vitals

- Pulse rate
- Respiratory rate
- Haemoglobin
- Systolic and diastolic blood pressure

### Reproductive and cycle information

- Cycle regularity
- Cycle length
- Marriage duration
- Pregnancy status
- Number of abortions

### Laboratory measurements

- Beta-HCG I and II
- FSH and LH
- FSH/LH ratio
- TSH
- AMH
- Prolactin
- Vitamin D3
- Progesterone
- Random blood sugar

### Symptoms and lifestyle

- Weight gain
- Hair growth
- Skin darkening
- Hair loss
- Pimples
- Fast-food consumption
- Regular exercise

### Ultrasound measurements

- Left and right follicle counts
- Left and right average follicle sizes
- Endometrial thickness

## Encoding notes

- Most `(Y/N)` columns use `0` for No and `1` for Yes.
- `Cycle(R/I)` mainly contains `2` and `4`; their precise meanings must be confirmed.
- `Cycle(R/I) = 5` appears once and is treated as suspicious.
- Blood groups are represented by codes `11` to `18`; their mapping is not documented.

## Known data-quality issues

- `Unnamed: 44` contains spreadsheet artifacts and should be removed.
- `Marraige Status (Yrs)` has one missing value.
- `Fast food (Y/N)` has one missing value.
- `II beta-HCG(mIU/mL)` contains `1.99.`
- `AMH(ng/mL)` contains `a`.
- Extremely low pulse and blood-pressure values require handling.
- Extreme FSH, LH, TSH and Vitamin D3 values require review.
- Derived columns include BMI, FSH/LH and waist-to-hip ratio.

