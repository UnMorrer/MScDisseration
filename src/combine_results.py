import os
import re
import pandas as pd
import datetime
import common.scraping as scrape
import common.config as cfg

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


def remove_newlines(input):
    """
    Function to remove newline characters to make the 2
    descriptions identical

    Inputs:
    input - str: The raw string

    Returns:
    cleanedInput - str: String
    with newline characters removed
    """

    cleanedInput = re.sub(r"\r?\n", "", input)
    return cleanedInput


# Combine them into one
def combine_tables(filePaths, 
                   addDate=True, 
                   removeNewline=True, 
                   unescapeDescription=False):
    """
    Function to take a list of paths and combine those
    (.csv) files together into a big table. Combines
    tables along the rows.

    Inputs:
    filePaths - [str]: List of filepath strings
    to read in and combine. Should be full/absolute
    paths.
    addDate - bool: Add date as new "date" column
    to the data
    unescapeDescription - bool: Unescape HTML tags
    and other characters in the jobDescription
    column

    Returns:
    combined_df - The combined output. Column names inferred
    from 1st list item.
    """

    dataframes = []

    for file in filePaths:
        df = pd.read_csv(file)

        # Extract date from name
        if addDate:
            date = file[-12:-4]
            dateObj = datetime.datetime.strptime(date, "%Y%m%d")
            df["date"] = dateObj
        
        if unescapeDescription:
            df["unescapedJobDesc"] = df.jobDescription.apply(scrape.html_to_text)
        
        if removeNewline:
            df["cleanContent"] = df.content.apply(remove_newlines)
            
        dataframes.append(df)

    # Combine dataframes together
    combined_df = pd.concat(dataframes, ignore_index=True)

    return combined_df


if __name__ == "__main__":
    searchDirectory = "/home/omarci/masters/MScDisseration/data"
    jobFileRegex = re.compile(r"JoobleData_\d{8}.csv")
    fullDescRegex = re.compile(r"JoobleData_FullDesc_\d{8}.csv")

    jobColumns = cfg.data_types.keys()
    descColumns = cfg.full_content_data_types.keys()

    jobFileList = get_all_files(jobFileRegex, searchDirectory)
    jobDescList = get_all_files(fullDescRegex, searchDirectory)

    jobDf = combine_tables(jobFileList, addDate=True, 
                           removeNewline=True, unescapeDescription=False)
    descDf = combine_tables(jobDescList, addDate=True, 
                            removeNewline=False, unescapeDescription=True)

    # Filter for unique jobs using uid column
    jobDf.drop_duplicates(subset="uid", inplace=True)
    jobDf = jobDf.rename(columns={"Unnamed: 0_x": "0"})
    descDf.drop_duplicates(subset="uid", inplace=True)

    # Join the two based on UID
    fullDf = pd.merge(jobDf, descDf, on="uid", how="inner")

    # Investigate what could not be joined together
    noJob = pd.merge(jobDf, descDf, on="uid", how="right", indicator=True)
    noJob = noJob[noJob["_merge"] == "right_only"]

    # Same for description
    noDesc = pd.merge(jobDf, descDf, on="uid", how="left", indicator=True)
    noDesc = noDesc[noDesc["_merge"] == "left_only"]

    # Try 2nd round of matching with date AND job description
    # noDesc - date_x has the date
    # noJob - date_y has the date

    # Rename some columns and remove others
    noJob = noJob.rename(columns={
        "0_y": "0",
        "date_y": "date",
    })
    noJob = noJob[descColumns]

    noDesc = noDesc.rename(columns={
        "0_x": "0",
        "date_x": "date",
    })
    noDesc = noDesc[jobColumns]

    a = 1

    # Save matched results
    # fullDf.to_csv("/home/omarci/masters/MScDisseration/data/merged_full.csv")
    # noDesc.to_csv("/home/omarci/masters/MScDisseration/data/merged_noDesc.csv")
    # noJob.to_csv("/home/omarci/masters/MScDisseration/data/merged_onlyDesc.csv")