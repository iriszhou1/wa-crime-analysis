"""
Iris Zhou
CSE 163
Tests methods to mutate dataframes and create new dataframes from the
crime_types.py file.
"""

import crime_types
from cse163_utils import assert_equals


def test_load_and_clean_crime_data(file_path):
    """
    Given file path to test data file, tests that after dataset has been
    cleaned, column names are all lower case and only relevant columns
    remain. Returns the resulting dataframe for further tests.
    """
    cleaned_df = crime_types.load_and_clean_crime_data(file_path)
    colnames = cleaned_df.columns

    # Test that column names are lower case
    assert_equals(False, 'YEAR' in colnames)
    assert_equals(False, 'ThEfT' in colnames)
    assert_equals(True, 'year' in colnames)
    assert_equals(True, 'theft' in colnames)

    # Test that unnecessary columns have been removed
    assert_equals(False, 'location' in colnames)
    assert_equals(False, 'prprtyrate' in colnames)

    return cleaned_df


def test_get_crime_totals(cleaned_df):
    """
    Given cleaned crime dataframe, tests that added crime totals column
    contains expected value.
    """
    crime_types.get_crime_totals(cleaned_df)
    assert_equals(21, cleaned_df.iloc[0]['crime_totals'])


def test_get_crime_type_rates(cleaned_df):
    """
    Given cleaned crime dataframe, uses get_crime_type_rates method
    to create new dataframe of relative crime rates.
    Tests that new dataframe has expected values.
    Returns resulting dataframe for further tests.
    """
    rate_df = crime_types.get_crime_type_rates(cleaned_df)
    assert_equals(1/21, rate_df.iloc[0]['murder'])
    assert_equals(1/21, rate_df.iloc[0]['theft'])
    return rate_df


def test_pivot_rate_data(rate_df):
    """
    Given dataframe of crime rates, uses pivot_rate_data method
    to convert dataframe to longer format.
    Tests that pivoted dataframe has the correct shape.
    Returns the resulting dataframe for further tests.
    """
    pivot_df = crime_types.pivot_rate_data(rate_df)
    assert_equals((21, 3), pivot_df.shape)
    return pivot_df


def main():
    test_file_path = 'data/test_crime.csv'

    cleaned_df = test_load_and_clean_crime_data(test_file_path)
    test_get_crime_totals(cleaned_df)
    rate_df = test_get_crime_type_rates(cleaned_df)
    test_pivot_rate_data(rate_df)


if __name__ == '__main__':
    main()
