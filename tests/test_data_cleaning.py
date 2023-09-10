import pandas as pd
import numpy as np
import pytest
from poll_tracker.data_cleaning.data_cleaning import DataCleaner

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'Pollster\n': ['A', 'B', '  C  '],
        '\n': ['\n', '\n', '\n'],
        'Date\n': ['3/30/24', '3/28/24', '3/27/24'],
        'sample': ['1000', '    2000    ', '3,000*'],
        'bulstrode': ['55.5%', '60.3%', '**'],
        'casaubon': ['44.5%', '39.7%', '40.7%'],
        'chettam': ['22%', '10%', np.nan], 
        'lydgate': ['32%', '42%', '38%'],
        'others': ['32%', '42%', '38%'], 
        'vincy': ['32%', '42%', '38%']
    })

def test_clean_data(sample_data):
    cleaner = DataCleaner(sample_data)
    cleaned_data = cleaner.clean_data()

    # Check if the columns have been cleaned and formatted as expected
    expected_columns = ['pollster', 'date', 'sample', 'bulstrode', 'casaubon', 'chettam', 
                        'lydgate', 'others', 'vincy', 'sample_exclusions', 'alt_survey']
    assert list(cleaned_data.columns) == expected_columns

    # Check if the 'Date' column has been converted to the correct date format
    # expected_dates = ['2024-03-30', '2024-03-28', '2024-03-27']
    # expected_dates_objects = pd.to_datetime(expected_dates)
    # assert list(cleaned_data['date']) == expected_dates_objects

    # Check if row values match for different candidate cleaning cases
    expected_values = [0.555, 0.603, np.nan]
    actual_values = list(round(cleaned_data['bulstrode'], 3))
    # Compare the lists with NaN handling
    for expected, actual in zip(expected_values, actual_values):
        if not (np.isnan(expected) and np.isnan(actual)) and expected != actual:
            # If expected and actual are not both NaN and they are not equal
            raise AssertionError("Values do not match.")
    
    expected_values = [0.22, 0.10, np.nan]
    actual_values = list(round(cleaned_data['chettam'], 3)) 
    # Compare the lists with NaN handling
    for expected, actual in zip(expected_values, actual_values):
        if not (np.isnan(expected) and np.isnan(actual)) and expected != actual:
            # If expected and actual are not both NaN and they are not equal
            raise AssertionError("Values do not match.")
    
    expected_values = [0.445, 0.397, 0.407]
    assert list(round(cleaned_data['casaubon'], 3)) == expected_values

    # Check if the 'sample' column has been cleaned and converted to integers
    expected_samples = [1000, 2000, 3000]
    assert list(cleaned_data['sample']) == expected_samples

    # Check if * and ** indicators are converted to new columns
    expected_sample_exclusions = [0, 0, 1]
    assert list(cleaned_data['sample_exclusions']) == expected_sample_exclusions
    expected_alt_survey = [0, 0, 1]
    assert list(cleaned_data['alt_survey']) == expected_alt_survey



