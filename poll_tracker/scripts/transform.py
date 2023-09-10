import pandas as pd
import os
from poll_tracker.data_cleaning.data_cleaning import DataCleaner

def main():
        
    # Get the current directory
    cwd_dir = os.getcwd()

    # Construct the absolute path to csv file
    raw_data_path = 'data/raw_polls.csv'
    absolute_path = os.path.join(cwd_dir, raw_data_path)

    # Check if the file exists
    if os.path.exists(absolute_path):
        # Read in file in as Pandas DataFrame
        df = pd.read_csv('data/raw_polls.csv')
    else:
        print(f"File not found at path: {absolute_path}")

    # Clean raw data
    cleaner = DataCleaner(df)
    cleaned_df = cleaner.clean_data()

    # Save file to CSV
    cleaned_data_path = 'data/cleaned_polls.csv'
    cleaned_df.to_csv(os.path.join(cwd_dir, cleaned_data_path), index=False)
    print("Cleaned data saved in", os.path.join(cwd_dir, cleaned_data_path))

