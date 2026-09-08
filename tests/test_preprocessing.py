import numpy as np
import pandas as pd

from pcosense.preprocessing import build_numeric_preprocessor


def test_preprocessor_handles_missing_values():
    data = pd.DataFrame({
        "age": [20, 30, np.nan, 40],
        "bmi": [21.0, np.nan, 25.0, 30.0],
    })

    preprocessor = build_numeric_preprocessor()
    transformed = preprocessor.fit_transform(data)

    assert transformed.shape == (4, 2)
    assert not np.isnan(transformed).any()