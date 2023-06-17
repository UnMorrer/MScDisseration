# Exploratory data analysis for jobs with full data
# - Language - deepl module
# - Salary
# - Country
# - Duplicate ads with cosine similarity
# - etc.

import pandas as pd
import deepl
import configparser

# Read in data
df = pd.read_csv("/home/omarci/masters/MScDisseration/data/merged_full.csv")
config = configparser.ConfigParser()
config.read(".env")
APIKey = config["DeepL"]["DEEPL_API_KEY"]
translator = deepl.Translator(APIKey)

# Character number in full description
print(f"Summary stats - number of characters in job description: \n")
print(df.jobDescription.str.len().describe())
# Min 25 - Max 14,542: Enormous range present BUT all below 15k character limit for translation

def translate_job(
        jobDescBatch,
        deepLTranslator,
        dest="EN-GB"):
    """
    Function to translate the job descriptions in batches
    using the DeepL Translate API

    Inputs:
    jobDescBatch - [str]: A list of job descriptions to be translated OR
    a single string that is translated
    deepLTranslator - deepl.Trnaslator : An object to handle the translation.
    dest - str: Destination language. More info here:
    https://github.com/DeepLcom/deepl-python

    Returns:
    texts - [str]: The translated texts
    sources - [str]: The list of source languages  
    """
    results = deepLTranslator.translate_text(
        jobDescBatch,
        target_lang=dest
    )
    
    # Separate results
    if type(results) == type([]):
        texts = []
        sources = []
        for item in results:
            texts.append(item.text)
            sources.append(item.detected_source_lang)
        
        return texts, sources
    
    # If only 1 string is translated
    return results.text, results.detected_source_lang

# TODO: Translation is pricey...
# For everything -> 13.8M characters ~ EUR 280
# Can do 1st 100 characters from each advert -> Within free tier
# Discuss options with supervisor

# Focus INSTEAD - remove duplicate advertisements

a = 1