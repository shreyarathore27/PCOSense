"""Feature groups used by the PCOSense models."""

TARGET_COLUMN = "PCOS (Y/N)"

ID_COLUMNS = [
    "Sl. No",
    "Patient File No.",
]

QUESTIONNAIRE_FEATURES = [
    "Age (yrs)",
    "BMI",
    "Cycle(R/I)",
    "Cycle length(days)",
    "Pregnant(Y/N)",
    "No. of aborptions",
    "Weight gain(Y/N)",
    "hair growth(Y/N)",
    "Skin darkening (Y/N)",
    "Hair loss(Y/N)",
    "Pimples(Y/N)",
    "Fast food (Y/N)",
    "Reg.Exercise(Y/N)",
]

VITAL_FEATURES = [
    "Pulse rate(bpm)",
    "RR (breaths/min)",
    "Hb(g/dl)",
    "BP _Systolic (mmHg)",
    "BP _Diastolic (mmHg)",
]

SCREENING_FEATURES = QUESTIONNAIRE_FEATURES + VITAL_FEATURES

LAB_FEATURES = [
    "I beta-HCG(mIU/mL)",
    "II beta-HCG(mIU/mL)",
    "FSH(mIU/mL)",
    "LH(mIU/mL)",
    "TSH (mIU/L)",
    "AMH(ng/mL)",
    "PRL(ng/mL)",
    "Vit D3 (ng/mL)",
    "PRG(ng/mL)",
    "RBS(mg/dl)",
]

ULTRASOUND_FEATURES = [
    "Follicle No. (L)",
    "Follicle No. (R)",
    "Avg. F size (L) (mm)",
    "Avg. F size (R) (mm)",
    "Endometrium (mm)",
]

SCREENING_PLUS_LABS_FEATURES = SCREENING_FEATURES + LAB_FEATURES

FULL_CLINICAL_FEATURES = (
    SCREENING_FEATURES
    + LAB_FEATURES
    + ULTRASOUND_FEATURES
)

FEATURE_SETS = {
    "screening": SCREENING_FEATURES,
    "screening_plus_labs": SCREENING_PLUS_LABS_FEATURES,
    "full_clinical": FULL_CLINICAL_FEATURES,
}

def validate_feature_sets(columns: list[str]) -> None:
    """Confirm that all configured features exist in the dataset."""

    available = set(columns)

    for name, features in FEATURE_SETS.items():
        missing = sorted(set(features) - available)

        if missing:
            raise ValueError(
                f"Feature set '{name}' has missing columns: {missing}"
            )