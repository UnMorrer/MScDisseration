import os
import re
import pandas as pd

# Get all files matching name pattern
def get_all_files(pattern, directory: str):
    """
    Function to match all files with pattern in directory

    Inputs:
    pattern - regex: Regular expression defining the matches
    directory - str: The directory to search for. Search is NON-RECURSIVE

    Returns:
    files - [str]: A list of strings with full filepaths that match
    the specified regex in the folder
    """
    files = []

    for fileName in os.listdir(directory):
        if pattern.match(fileName):
            absPath = os.path.join(directory, fileName)
            files.append(absPath)
    
    return files

# Combine them into one
def combine_tables(filePaths):
    """
    Function to take a list of paths and combine those
    (.csv) files together into a big table. Combines
    tables along the rows.

    Inputs:
    filePaths - [str]: List of filepath strings
    to read in and combine. Should be full/absolute
    paths.

    Returns:
    combined_df - The combined output. Column names inferred
    from 1st list item.
    """

    dataframes = []

    for file in filePaths:
        df = pd.read_csv(file)
        dataframes.append(df)

    # Combine dataframes together
    combined_df = pd.concat(dataframes, ignore_index=True)

    return combined_df

def unescape_description(jobDesc):
    """
    Function to unescape job description scraped 
    (which includes HTML tags)
    """
    # use html_to_text from scraping.py in common folder
    pass

def unescape_content(jobDesc):
    """
    Function to unescape job content scraped 
    (may not be needed - check encoding)
    """

if __name__ == "__main__":
    searchDirectory = "/home/omarci/masters/MScDisseration/data"
    jobFileRegex = re.compile(r"JoobleData_\d{8}.csv")
    fullDescRegex = re.compile(r"JoobleData_FullDesc_\d{8}.csv")

    jobFileList = get_all_files(jobFileRegex, searchDirectory)
    jobDescList = get_all_files(fullDescRegex, searchDirectory)

    jobDf = combine_tables(jobFileList)
    descDf = combine_tables(jobDescList)

    # Filter for unique jobs using uid column
    jobDf.drop_duplicates(subset="uid", inplace=True)
    descDf.drop_duplicates(subset="uid", inplace=True)

    # Join the two based on UID
    fullDf = pd.merge(jobDf, descDf, on="uid", how="inner")

    # Investigate what could not be joined together
    noJob = pd.merge(jobDf, descDf, on="uid", how="right", indicator=True)
    noJob = noJob[noJob["_merge"] == "right_only"]

    # Same for description
    noDesc = pd.merge(jobDf, descDf, on="uid", how="left", indicator=True)
    noDesc = noDesc[noDesc["_merge"] == "left_only"]

    # Save matched results
    fullDf.to_csv("/home/omarci/masters/MScDisseration/data/merged_full.csv")
    noDesc.to_csv("/home/omarci/masters/MScDisseration/data/merged_noDesc.csv")
    noJob.to_csv("/home/omarci/masters/MScDisseration/data/merged_onlyDesc.csv")