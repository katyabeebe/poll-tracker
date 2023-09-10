import pandas as pd
import numpy as np
import pytest
from poll_tracker.data_transform.data_transform import DataTransformer

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'pollster': ['a', 'b', 'c'],
        'date': ['2024-03-30', '2024-03-28', '2024-03-26'],
        'sample': ['1000', '2000', '3000'],
        'bulstrode': [.555, .603, np.nan],
        'casaubon': [.445, .397, .407],
        'chettam': [.22, .1, np.nan], 
        'lydgate': [.32, .42, .38],
        'others': [.32, .42, .38], 
        'vincy': [.32, .42, .38],
        'sample_exclusions': [0, 0, 1],
        'alt_survey': [0, 0, 1]
    })

def test_clean_data(sample_data):
    transformer = DataTransformer(sample_data)
    transformed_data = transformer.transform_data()

    # Check if the columns have been cleaned and formatted as expected
    expected_columns = ['date',  'bulstrode', 'casaubon', 'chettam', 
                        'lydgate', 'others', 'vincy']
    assert list(transformed_data.columns) == expected_columns
