import os
import re
import pandas as pd
import datetime
import bs4
import common.config as cfg
import datetime as dt

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


def clean_html(text):
    """
    Function to clean HTML text from tags and
    unescape HTML characters. Keeps newlines
    in original html
    """
    return bs4.BeautifulSoup(text, "html.parser").get_text("\n")


def extract_uid_from_url(url):
    """
    Function to extract job UID from job URL

    Inputs:
    url - string: The job URL

    Returns:
    uid - int: The job's unique ID
    """
    parts = url.replace("?", "/").split("/")
    uid = parts[4]
    return int(uid)

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
            df["unescapedJobDesc"] = df.jobDescription.apply(clean_html)
        
        if removeNewline:
            df["cleanContent"] = df.content.apply(remove_newlines)
            
        dataframes.append(df)

    # Combine dataframes together
    combined_df = pd.concat(dataframes, ignore_index=True)

    return combined_df


if __name__ == "__main__":
    searchDirectory = "/home/omarci/masters/MScDissertation/data"
    jobFileRegex = re.compile(r"JoobleData_\d{8}.csv")
    fullDescRegex = re.compile(r"JoobleData_FullDesc_\d{8}.csv")

    jobColumns = list(cfg.data_types.keys()) 
    jobColumns += ["date", "cleanContent"]
    descColumns = list(cfg.full_content_data_types.keys()) + ["id"]
    descColumns += ["date", "unescapedJobDesc"]

    jobFileList = get_all_files(jobFileRegex, searchDirectory)
    jobDescList = get_all_files(fullDescRegex, searchDirectory)

    jobDf = combine_tables(jobFileList, addDate=True, 
                           removeNewline=True, unescapeDescription=False)
    descDf = combine_tables(jobDescList, addDate=True, 
                            removeNewline=False, unescapeDescription=True)
    
    descDf.drop(descDf[descDf['uid'] == "uid"].index, inplace=True) # -> some are "uid"
    # Descsription UIDs retrieved as string - NOT the best for ensuring records are intact
    # See problems below...

    # Filter for unique jobs using uid column
    jobDf.drop_duplicates(subset="uid", inplace=True)
    # ALL uids in jobDf match that extracted from the URL
    jobDf = jobDf.rename(columns={"Unnamed: 0_x": "0"})
    descDf.drop_duplicates(subset="uid", inplace=True)

    print(f"Total jobs: {jobDf.shape[0]}") #-> 6139
    print(f"Total descriptions: {descDf.shape[0]}") #-> 5556
    print(f"Unique IDs in jobs df: {len(jobDf.uid.unique())}") #-> 6139
    print(f"Unique IDs in descriptions df: {len(descDf.uid.unique())}") #-> 5556

    # Save all descriptions for InfoShield analysis
    descDf["id"] = descDf.index + 1 # create ID to enable tracking in InfoShield
    descDf.to_csv("/home/omarci/masters/MScDissertation/data/all_descriptions.csv", encoding='utf-8-sig')

    # Join the two based on UID and date
    fullDf = pd.merge(jobDf, descDf, on="uid", how="inner")
    print(f"jobDf date =/= descDf date, UID join: {sum(fullDf.date_x != fullDf.date_y)}") # -> 445
    fullDf["dateDiff"] = fullDf.date_x - fullDf.date_y
    # Examining time delta
    print(f"Number of records with more than 2 days difference: {sum(abs(fullDf.dateDiff) >= dt.timedelta(days=2))}") # -> 295
    # Drop if more than 2 days apart -> unlikely match
    fullDf.drop(fullDf[abs(fullDf.dateDiff) >= dt.timedelta(days=2)].index, inplace=True)
    print(f"Matched on date + UID: {fullDf.shape[0]}")# -> 3334
    fullDf.drop(columns="dateDiff", inplace=True)


    # Investigate what could not be joined together
    noJob = pd.merge(jobDf, descDf, on="uid", how="right", indicator=True)
    noJob = noJob[noJob["_merge"] == "right_only"]

    # Same for description
    noDesc = pd.merge(jobDf, descDf, on="uid", how="left", indicator=True)
    noDesc = noDesc[noDesc["_merge"] == "left_only"]

    print(f"No job: {noJob.shape[0]}") #-> 1927
    print(f"No description: {noDesc.shape[0]}") #-> 2510

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

    # Create new "content" column that is first 40 characters of description
    noJob["shortContent"] = noJob.unescapedJobDesc.str.slice(0, 40)
    noDesc["shortContent"] = noDesc.cleanContent.str.slice(0, 40)
    # All shortContent unique - NOPE
    # BUT date + shortContent IS unique

    # Enforce 1:1 merge
    noDesc.drop_duplicates(subset=["date", "shortContent"], inplace=True)
    noJob.drop_duplicates(subset=["date", "shortContent"], inplace=True)

    # Try another merge
    mergeDf2 = pd.merge(noJob, noDesc, on=["date", "shortContent"], how="outer", indicator=True)
    merged2 = mergeDf2[mergeDf2._merge == 'both']
    unMerged2 = mergeDf2[mergeDf2._merge != 'both']

    # Shapes
    print(f"Matched on UID: {fullDf.shape[0]}")
    print(f"Matched on date + desc: {mergeDf2[mergeDf2._merge == 'both'].shape[0]}")

    # Non-matching dates in UID match:
    # print(f"Nonmatching dates, UID join: {fullDf[fullDf.date_x != fullDf.date_y].shape[0]}")

    # Combine matches
    merged2.rename(inplace=True,
                   columns={
        "uid_y": "uid",
    })
    fullDf.rename(inplace=True, columns={
        "date_y": "date",
    })
    fullDf.drop(inplace=True, columns=["Unnamed: 0_x", "date_x", "Unnamed: 0_y"])

    merged2 = merged2[fullDf.columns]
    mergedDf = pd.concat([fullDf, merged2], ignore_index=True)

    # Drop NA job descriptions
    mergedDf.dropna(subset=["unescapedJobDesc"], inplace=True)

    # Save matched results
    mergedDf.to_csv("/home/omarci/masters/MScDissertation/data/merged_full.csv", encoding='utf-8-sig')
    unMerged2.to_csv("/home/omarci/masters/MScDissertation/data/unMerged_round2.csv", encoding='utf-8-sig')

    # Further investigation bits:
    # Some values in descDf are "uid" - strange.... -> happened because was collected as string
    # + Related issue - some numbers had scientific notation or missing digits

    # NOTE: What if... join desc and job df on a daily basis -> considered, just use
    # date variable to achieve same effect

    a = 1