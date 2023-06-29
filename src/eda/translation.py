import deep_translator as dptrans
import pandas as pd
import random as rnd
import numpy as np
import time

merged_data_filepath = "/home/omarci/masters/MScDisseration/data/merged_full.csv"
translations_filepath = "/home/omarci/masters/MScDisseration/data/translated_descriptions.csv"

# TODO: Look into LOCAL translation, or at least language detection
# Translation lib: https://pypi.org/project/deep-translator/
# Detection (local) lib: https://towardsdatascience.com/develop-a-text-language-detector-and-translator-system-in-python-6537d6244b10
# --> Module: cld3 - https://github.com/google/cld3

df = pd.read_csv(merged_data_filepath)
translatedDescriptions = pd.read_csv(translations_filepath, index_col=False)
batchSize = 10

def translate_job_deepl(
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
    # Cosine similarity
    # Clustering with InfoShield - language indep. -> on its way

    # APIKey = config["DeepL"]["DEEPL_API_KEY"]
    # translator = deepl.Translator(APIKey)


def translate_job_deeptrans(
        jobDescBatch,
        source="auto",
        dest="en"):
    """
    Function to translate the job descriptions in batches
    using the DeepL Translate API

    Inputs:
    jobDescBatch - [str]: A list of job descriptions to be translated
    dest - str: Destination language. More info here:
    https://github.com/DeepLcom/deepl-python

    Returns:
    texts - [str]: The translated texts 
    """

    texts = dptrans.GoogleTranslator(source=source, target=dest).translate_batch(jobDescBatch)
    return texts


def translate_in_batches(
        df,
        excludeIds,
        batchSize=10
):
    """
    Function to handle bulck of batch translation

    Inputs:
    df - pd.DataFrame: A pandas DataFrame with at least
    2 columns - id, cleanContent. One holds a unique 
    identifier while the other has the texts to be
    translated.
    excludeIDs - [int]: A list of integer identifiers
    that are to be excluded in the sampling

    Returns:
    translatedText - pd.DataFrame: A pandas DataFrame
    of size batchSize with 2 columns: id and translatedJobDesc
    that each hold a unique identifier and the translated job
    description
    """

    outdf = pd.DataFrame()

    # Exclude IDs not needed
    selectiondf = df[~df['id'].isin(excludeIds)]
    
    # Randomly  select batchSize number of IDs
    selectedIds = rnd.sample(selectiondf.id.tolist(), batchSize)

    selectiondf = df[df['id'].isin(selectedIds)]
    outdf["id"] = selectiondf.id
    outdf["translatedJobDesc"] = translate_job_deeptrans(selectiondf.cleanContent.tolist())
    
    return outdf


if __name__ == "__main__":
    loopsLeft = int(np.ceil((df.shape[0] - translatedDescriptions.shape[0])/batchSize))

    for i in range(1):
        try:
            # Translate stuff
            returndf = translate_in_batches(df, translatedDescriptions.id.tolist(), batchSize=batchSize)

            # Capture results
            translatedDescriptions = pd.concat(translatedDescriptions, returndf)
        except Exception as e:
            # Save if error
            translatedDescriptions.to_csv(translations_filepath)
            print(f"Error occurred: {e}")

        print(f"Translation of batch {i} done")
        print(f"Progress: {i*batchSize}/{(df.shape[0] - translatedDescriptions.shape[0])}")

        # Wait between tries
        time.sleep(batchSize)