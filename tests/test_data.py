import pandas as pd

from pcosense.data import clean_base_data
from pcosense.features import FEATURE_SETS, ID_COLUMNS, TARGET_COLUMN


def test_clean_base_data_handles_known_errors():
    raw = pd.DataFrame({
        " Cycle(R/I) ": [5],
        "Cycle length(days)": [0],
        "Pulse rate(bpm)": [13],
        "BP _Systolic (mmHg)": [12],
        "BP _Diastolic (mmHg)": [8],
        "FSH(mIU/mL)": [5052],
        "LH(mIU/mL)": [2018],
        "Vit D3 (ng/mL)": [6014.66],
        "II  beta-HCG(mIU/mL)": ["1.99."],
        "AMH(ng/mL)": ["a"],
        "Unnamed: 44": ["."],
    })

    cleaned = clean_base_data(raw)

    assert "Unnamed: 44" not in cleaned.columns
    assert "Cycle(R/I)" in cleaned.columns

    columns_expected_missing = [
        "Cycle(R/I)",
        "Cycle length(days)",
        "Pulse rate(bpm)",
        "BP _Systolic (mmHg)",
        "BP _Diastolic (mmHg)",
        "FSH(mIU/mL)",
        "LH(mIU/mL)",
        "Vit D3 (ng/mL)",
        "II beta-HCG(mIU/mL)",
        "AMH(ng/mL)",
    ]

    assert cleaned[columns_expected_missing].isna().all().all()

    from pcosense.features import (
    FEATURE_SETS,
    ID_COLUMNS,
    TARGET_COLUMN,
)


def test_feature_sets_exclude_identifiers_and_target():
    forbidden = set(ID_COLUMNS + [TARGET_COLUMN])

    for features in FEATURE_SETS.values():
        assert not forbidden.intersection(features)
        assert len(features) == len(set(features))


def test_feature_sets_have_expected_sizes():
    assert len(FEATURE_SETS["screening"]) == 18
    assert len(FEATURE_SETS["screening_plus_labs"]) == 28
    assert len(FEATURE_SETS["full_clinical"]) == 33

    