import pandas as pd
import numpy as np

class DataTransformer:
    """
    A class for transforming cleaned polling data into averages. 
    """

    def __init__(self, data: pd.DataFrame):
        self.data = data

    def transform_data(self):
        """Run all data transformation methods."""
        self.drop_alt_survey_polls()
        self.handle_outliers()
        self.apply_weighted_average_by_day()
        # self.fill_in_missing_dates()
        return self.data

    def drop_alt_survey_polls(self):
        """Drop polls which offered alternative versions."""
        self.data = self.data[self.data.alt_survey == 0]

    def handle_outliers(self):
        """Identify outliers according to 2 standard deviations from the mean calculated on a 
        weekly level in order to provide a longer-term trend view.
        Note: dropping outliers is not the best practice. I would try windsorising in a future
        version. 
        """
        df_long = transform_wide_to_long(self.data)
        outlier_rows = identify_weekly_outliers(df_long, 'poll_value', 'date')
        # Identify and drop outliers based on the bounds
        # Alternatively, we should try windsorising instead of dropping these data points
        mask = self.data.index.isin(outlier_rows.index)
        # Drop rows identified by the mask
        self.data = self.data[~mask]

    def apply_weighted_average_by_day(self):
        """Take a weighted avergae for each polled date. The weights come from the 
        sample sizes. Using these sample sizes, I also assume that the polls that exclude 
        overseas territories should be slightly downweighted."""
        df_long = transform_wide_to_long(self.data)
        df_weighted = weighted_average_by_day(df_long, 'candidate', 'poll_value', 'sample')
        self.data = transform_long_to_wide(df_weighted)

    def fill_in_missing_dates(self):
        """Fill in missing dates with the last available value. The longest stretch in missing 
        dates is 7, with a majority being 1-2 days."""
        df_w_all_dates = create_full_date_range(self.data, 'date')
        # Fill NaNs only for rows where all values are NaN
        # Identify rows where all values are NaN
        all_nan_rows = df_w_all_dates[df_w_all_dates.isnull().all(axis=1)] 
        df_w_all_dates.loc[all_nan_rows.index] = all_nan_rows.ffill()
        self.data = df_w_all_dates


def transform_wide_to_long(df):
    return df.melt(id_vars=['date', 'pollster', 'sample', 'sample_exclusions', 'alt_survey'], var_name='candidate', value_name='poll_value')

def transform_long_to_wide(df):
    df_wide = df.pivot(index='date',columns='candidate', values='weighted_avg').reset_index() 
    df_wide.columns.name = None
    return df_wide


def identify_weekly_outliers(df, value_column, date_column, std_dev_threshold=2):
    # Convert the date column to a datetime type
    df[date_column] = pd.to_datetime(df[date_column])

    # Create a week column to group by
    df['Week'] = df[date_column].dt.strftime('%Y-%U')

    # Group the data by week and calculate the mean and standard deviation
    grouped = df.groupby('Week')[value_column].agg(['mean', 'std']).reset_index()

    # Calculate the lower and upper bounds for identifying outliers
    grouped['lower_bound'] = grouped['mean'] - std_dev_threshold * grouped['std']
    grouped['upper_bound'] = grouped['mean'] + std_dev_threshold * grouped['std']

    # Merge the outlier bounds back to the original DataFrame
    df = df.merge(grouped[['Week', 'lower_bound', 'upper_bound']], on='Week', how='left')

    # Identify outliers based on the bounds
    outliers = df[(df[value_column] < df['lower_bound']) | (df[value_column] > df['upper_bound'])]

    return outliers

def weighted_average_by_day(df, candidate_col, value_column, sample_size_col):
    # Convert columns to numeric if needed
    df[value_column] = pd.to_numeric(df[value_column], errors='coerce')
    df[sample_size_col] = pd.to_numeric(df[sample_size_col], errors='coerce')
    
    # Calculate the weighted share for each row
    df['weighted_share'] = df[value_column] * df[sample_size_col]

    # Group the data by date and candidate and apply the weighted average function
    result = df.groupby(['date', candidate_col]).apply(
        lambda group: (group['weighted_share'] / group[sample_size_col].sum()).sum()
    ).reset_index(name='weighted_avg')

    # Replace 0s with NaNs
    result['weighted_avg'] = result['weighted_avg'].replace(0, np.nan)

    return result

def create_full_date_range(df, date_column):
    # Ensure datetime type
    df['date'] = pd.to_datetime(df['date'])

    # Find the minimum and maximum dates in the existing data
    min_date = df[date_column].min()
    max_date = df[date_column].max()

    # Generate a continuous date range from the minimum to the maximum date
    full_date_range = pd.date_range(start=min_date, end=max_date)

    # Create a DataFrame with the full date range
    full_date_df = pd.DataFrame({date_column: full_date_range})

    # Merge the original DataFrame with the full date range DataFrame
    merged_df = full_date_df.merge(df, on=date_column, how='left')

    return merged_df

