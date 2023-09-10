import pandas as pd
import numpy as np
from typing import List


class DataCleaner:
    """
    A class for cleaning and preprocessing tabular polling data.        
    This class provides methods for cleaning and transforming data in a Pandas DataFrame.
    It includes methods for removing newlines, stripping whitespace, converting
    columns to lowercase, handling exceptional cleaning tasks, and more.

    Example Usage:
    -------------
    # Run all cleaning operations
    cleaner.clean_data()

    # Display the cleaned data
    cleaner.display_data()
    """
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def clean_data(self):
        """Run all data cleaning methods."""
        self.remove_newlines_from_columns()
        self.strip_and_lowercase_columns()
        self.remove_newlines_from_data()
        self.replace_empty_with_nan()
        self.remove_empty_columns()
        self.strip_string_values()
        self.convert_date_column_to_datetime('date')
        self.clean_sample_column('sample')
        self.clean_candidate_columns(['bulstrode', 'casaubon', 'chettam', 'lydgate', 'others', 'vincy'])
        return self.data

    def remove_newlines_from_columns(self):
        """Remove newlines from column names."""
        self.data.columns = [c.replace("\n", "") for c in self.data.columns]

    def strip_and_lowercase_columns(self):
        """Strip leading/trailing spaces and convert column names to lowercase."""
        self.data.columns = self.data.columns.str.strip().str.lower()

    def remove_newlines_from_data(self):
        """Remove newlines from data cells."""
        self.data = self.data.replace('\n', '', regex=True)

    def replace_empty_with_nan(self):
        """Replace empty values with NaN."""
        self.data.replace('', np.nan, inplace=True)

    def remove_empty_columns(self):
        """Remove columns with all empty rows."""
        self.data = self.data.dropna(axis=1, how='all')

    def strip_string_values(self):
        """Strip leading/trailing spaces from string values."""
        self.data = self.data.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    def convert_date_column_to_datetime(self, column_name: str):
        """Convert the `date` column to datetime format."""
        self.data[column_name] = pd.to_datetime(self.data[column_name], format='mixed')

    def clean_sample_column(self, column_name: str):
        """A method to handle exceptional cleaning of the `sample` column."""
        # Function to check for '*'
        def has_asterisk(value):
            if '*' in value:
                return 1
            else:
                return 0

        # Create new column to indicate sample exclusions
        self.data['sample_exclusions'] = self.data[column_name].apply(has_asterisk)

        # Remove commas and * and convert to integers
        self.data[column_name] = self.data[column_name].str.replace(',', '').str.replace('*', '').astype('Int64')
    
    def clean_candidate_columns(self, column_names: List[str]):
        """A method to handle exceptional cleaning of the candidate columns. 
        Candidates columns: bulstrode, casaubon, chettam, lydgate, others, vincy""" 
        # Function to check for '**' in an element
        def has_double_asterisk(value):
            return 1 if '**' in value else 0

        # selected_cols = self.data[column_names].columns.to_list()

        # Create new column to indicate pollster used alternative surveys
        self.data['alt_survey'] = self.data[column_names].applymap(lambda x: int(isinstance(x, str) and '**' in x)).max(
            axis=1)

        # Remove **
        self.data.replace('**', np.nan, inplace=True)

        # Remove % and convert to decimal
        for col in column_names:
            self.data[col] = self.data[col].str.replace('%', '').apply(lambda x: float(x) / 100 if x else None)

    def display_data(self):
        """Display the cleaned data."""
        print(self.data)