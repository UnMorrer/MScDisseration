import re
import os
import pandas as pd

def load_previous_data(
        folder_path,
        filename_regex="*",
        regex_kwargs={},
        read_csv_kwargs={}):
    """
    Function to load scraping results from previous days

    Inputs:
    folder - str: Path to the folder storing the output .csv
    files from the previous days.
    filename_regex - str: Regular expression that defines the
    filenames. All filenames matching this RegEx will be loaded.
    If no input is given, ALL files in the folder will be read in.
    regex_kwargs - Arguments to be passed into the re.compile
    read_csv_kwards - Arguments to be passed to pd.read_csv().

    Returns:
    df - DataFrame: A DataFrame that contains all matching files
    (tables/dataframes), concatenated into one.
    """

    # Get the list of all files in the directory
    file_list = os.listdir(folder_path)

    # Keep only filenames that match
    regex = re.compile(filename_regex, **regex_kwargs)
    matching_files = list(filter(regex.match, file_list))

    # Concatenate previous results into BIG dataframe
    df = pd.DataFrame()

    for file_name in matching_files:
        file_path = os.path.join(folder_path, file_name)

        # Read (.csv) file into dataframe
        new_df = pd.read_csv(file_path, **read_csv_kwargs)

        df = pd.concat([df, new_df],ignore_index=True)

    # Keep only unique rows
    df = df.drop_duplicates()

    return df
