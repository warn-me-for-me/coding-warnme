import pandas as pd
import numpy as np
import math
from sklearn.metrics import cohen_kappa_score
import itertools
from pathlib import Path

def calculate_fleiss_kappa(df, columns):
    """
    Calculate Fleiss' kappa for the given set of columns in the DataFrame.

    Parameters:
    df (pandas.DataFrame): The input DataFrame.
    columns (list): A list of column names representing the annotators.
    none (bool): Include 'none' codes or not

    Returns:
    float: The Fleiss' kappa value.
    """
    # Group columns by annotator
    grouped_columns = group_columns_by_annotator(columns)

    # Get list of all possible codes
    codes = get_codes(df, columns)

    # Calculate the total number of items (documents/annotations)
    total_items = df.shape[0]

    # Initialize concordant_pairs
    concordant_pairs = 0

    for _, row in df.iterrows():
        row_values = []
        for annotator_columns in grouped_columns.values():
            annotator_values = row[annotator_columns].dropna().unique()
            if len(annotator_values) > 0:
                row_values.append(annotator_values[0])  # Take the first value for the annotator

        if len(row_values) > 1:
            # Generate all unique pairs of annotator ratings
            pairs = itertools.combinations(row_values, 2)

            # Count the number of pairs that agree
            concordant_pairs += sum(pair[0] == pair[1] for pair in pairs)

    # Calculate the total number of annotator pairs
    total_pairs = total_items * (len(grouped_columns) * (len(grouped_columns) - 1)) / 2
    value_counts = pd.concat([df[col] for col in columns]).value_counts(normalize=True)

    # Calculate the marginal probabilities pj
    pj = [value_counts.get(code, 0) for code in codes]

    # Calculate the expected proportion of concordant pairs due to chance
    pe = sum([p ** 2 for p in pj])

    # Calculate the proportion of concordant pairs
    pbar = concordant_pairs / total_pairs

    # Calculate the Fleiss' kappa
    kappa = (pbar - pe) / (1 - pe)

    return kappa

def group_columns_by_annotator(columns):
    """
    Group columns by annotator, considering columns with the same suffix as the same annotator.

    Parameters:
    columns (list): A list of column names representing the annotators.

    Returns:
    dict: A dictionary where the keys are annotator suffixes, and the values are lists of column names for that annotator.
    """
    grouped_columns = {}
    for col in columns:
        suffix = col.split('_')[-1]  # Assuming the suffix is the part after the last underscore
        if suffix not in grouped_columns:
            grouped_columns[suffix] = []
        grouped_columns[suffix].append(col)
    return grouped_columns

def get_codes(df, columns):
    """
    Get unique values across multiple columns in a DataFrame.

    Parameters:
    df (pandas.DataFrame): The input DataFrame.
    columns (list): A list of column names to get unique values from.

    Returns:
    numpy.ndarray: A 1D array of unique values across the specified columns.
    """
    unique_values = []
    for col in columns:
        unique_values.extend(df[col].unique())
    unique_values = np.unique(unique_values)
    return unique_values

def select_highest_agreement_code(df, columns, prefix1, prefix2=None):
    """
    Select the highest agreement code and optionally the second highest agreement code for each item/document,
    and assign them to separate columns.

    Parameters:
    df (pandas.DataFrame): The input DataFrame.
    columns (list): A list of column names representing the annotators.
    prefix1 (str): The prefix for the new column name containing the highest agreement code.
    prefix2 (str, optional): The prefix for the new column name containing the second highest agreement code.

    Returns:
    pandas.DataFrame: The updated DataFrame with one or two new columns containing the highest and second highest agreement codes.
    """
    # Group columns by annotator
    grouped_columns = group_columns_by_annotator(columns)

    # Initialize new column with NaN values
    new_column_name1 = f"{prefix1}_all"
    df[new_column_name1] = pd.Series([np.nan] * df.shape[0], index=df.index)

    # Initialize second new column with NaN values if prefix2 is provided
    if prefix2 is not None:
        new_column_name2 = f"{prefix2}_all"
        df[new_column_name2] = pd.Series([np.nan] * df.shape[0], index=df.index)

    for idx, row in df.iterrows():
        row_values = []
        for annotator_columns in grouped_columns.values():
            annotator_values = row[annotator_columns].dropna().unique()
            if len(annotator_values) > 0:
                row_values.append(annotator_values[0])  # Take the first value for the annotator

        if len(row_values) > 1:
            # Get the most frequent (highest agreement) code
            value_counts = pd.Series(row_values).value_counts()
            highest_agreement_code = value_counts.index[0]

            # Assign the highest agreement code to the new column
            df.at[idx, new_column_name1] = highest_agreement_code

            # If prefix2 is provided, assign the second highest agreement code to the second new column
            if prefix2 is not None:
                second_highest_agreement_code = value_counts.index[1] if len(value_counts.index) > 1 else np.nan
                df.at[idx, new_column_name2] = second_highest_agreement_code

    return df