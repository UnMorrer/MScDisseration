import deep_translator as dptrans
import pandas as pd
import random as rnd
import numpy as np
import time
import gcld3

merged_data_filepath = "/home/omarci/masters/MScDisseration/data/merged_full.csv"
translations_filepath = "/home/omarci/masters/MScDisseration/data/translated_descriptions.csv"
detection_filepath = "/home/omarci/masters/MScDisseration/data/lang_detection_output.csv"
merged_translated_data_filepath = "/home/omarci/masters/MScDisseration/data/merged_translated_full.csv"

# Translation lib: https://pypi.org/project/deep-translator/
# Detection (local) lib: https://towardsdatascience.com/introduction-to-googles-compact-language-detector-v3-in-python-b6887101ae47
# gcld3 on PyPi

df = pd.read_csv(merged_data_filepath)
print(f"Number of nonexistent job descriptions: {sum(df.unescapedJobDesc.isna())}") # 20
df.dropna(inplace=True, subset=["unescapedJobDesc"])
# translatedDescriptions = pd.read_csv(translations_filepath, index_col=False)
# translatedDescriptions = translatedDescriptions[["id", "translatedJobDesc"]]
detectionDf = df[["id", "unescapedJobDesc"]]

# Translation settings
batchSize = 10
translate = True # Enable/do translation

# Language detection settings
detectLang = True
detector = gcld3.NNetLanguageIdentifier(
    min_num_bytes=10,
    max_num_bytes=1000 #Truncates after
)

joinResults = True
a = 1

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
    time.sleep(1)
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
    outdf["translatedJobDesc"] = translate_job_deeptrans(selectiondf.unescapedJobDesc.tolist())
    
    return outdf


def detect_language(row, detector):
    """
    Function to detect input language of text

    Inputs:
    detector - gcld3.NNetLanguageIdentifier: Object that
    handles language detection, initialized outside function
    row - pd.Series: A row from the DataFrame. Must contain
    the unescapedJobDesc column as that's used for translation
    purposes.

    Returns:
    lang - str: BCP-47 language code of most
    probable language
    prob - float: Probability of text being
    in given language
    """
    result = detector.FindLanguage(text=row.unescapedJobDesc)
    lang = result.language
    prob = result.probability
    
    return (lang, prob)

# Post-hoc inspect translatedDescriptions
# print(f"Summary stats: {translatedDescriptions.translatedJobDesc.describe()}")
# print(f"Longest translation length: {max(translatedDescriptions.translatedJobDesc.str.len())}")
# print(f"Shortest translation length: {min(translatedDescriptions.translatedJobDesc.str.len())}")
# print(f"NA translations: {sum(translatedDescriptions.translatedJobDesc.isna())}")
# print(f"Top translations: {translatedDescriptions.translatedJobDesc.value_counts()}")

# Drop Error 400 rows
# translatedDescriptions = translatedDescriptions[~translatedDescriptions['translatedJobDesc'].str.startswith("Error 400")]

# Maximum translation can handle is 5000 characters - check how limiting this is...
print(f"Number of job descriptions above 5000 characters: {sum(df.unescapedJobDesc.str.len() >= 5000)}") #209
# Can we save them? Seems like a lot are in English?
saveIds = df[df.unescapedJobDesc.str.len() >= 5000].id

if __name__ == "__main__":
    if translate:
        for i in range(df.shape[0]):
            try:
                # Translate stuff
                # returndf = translate_in_batches(df[["id", "unescapedJobDesc"]], translatedDescriptions.id.tolist(), batchSize=batchSize)
                df["translatedJobDesc"] = df.apply(lambda row: pd.Series(translate_job_deeptrans([row["unescapedJobDesc"]])), axis=1)

                # Capture results
                # translatedDescriptions = pd.concat([translatedDescriptions, returndf])
            except Exception as e:
                # Save if error
                df.to_csv(translations_filepath)
                print(f"Error occurred: {e}")

            print(f"Translation of item {i} done")
            print(f"Progress: {i*batchSize}/{df.shape[0]}")

            # Wait between tries
            time.sleep(batchSize)
        
        # Save results
        df.to_csv(translations_filepath)
    
    if detectLang:
        detectionDf[['descLanguage', 'languageProb']] = detectionDf.apply(lambda row: pd.Series(detect_language(row, detector)), axis=1)
        detectionDf.to_csv(detection_filepath)

    #Join results together
    if joinResults:
        # df - 4878 x 43
        # translatedDescriptions - 4903 x 5
        # detectionDf - 4878 x 5
        detectionDf = pd.read_csv(detection_filepath)

        df["id"] = df.id.astype(int)
        languageDf = df.merge(detectionDf[["id", "descLanguage", "languageProb"]], on=["id"], how="left")

        # Summary stats about language
        print(f"Language counts: {languageDf.descLanguage.value_counts()}")
        # 60% Hungarian, 30% English, 5% German - 5% Other
        # (Other: lithuanian, polish, russian, ukrainian, romanian, french)
        languageDf.languageProb.describe()
        # Predictor is confident: 5 values below 50% probability
        # 0% - id 112: 1-word ad "Lakatos"
        # Rest below 50% are slavic (polish) + English mixed together

        # On joining back, look for nan translatedJobDesc and replace with English jobs...
        languageDf[languageDf.unescapedJobDesc.str.len() >= 5000].descLanguage.value_counts()
        # Above has 28 values, below has 209 values
        # WHY?
        saveIds = df[df.unescapedJobDesc.str.len() >= 5000].id

        # Track by ID
        languageDf[languageDf.id.isin(saveIds.tolist())].descLanguage.value_counts()

        # NOTE: Exclude jobs with fewer than 200 characters in description
        languageDf.to_csv(merged_translated_data_filepath)

        a = 1