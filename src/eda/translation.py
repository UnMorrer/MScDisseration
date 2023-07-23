import deep_translator as dptrans
import pandas as pd
import random as rnd
import numpy as np
import time
import gcld3
import itertools

# NOTE: Job descriptionss with more than 5000 characters
# or those with more than 200 characters were removed
# NOTE: Detected English job descriptions are/were NOT translated

merged_data_filepath = "/home/omarci/masters/MScDissertation/data/all_descriptions.csv"
translations_filepath = "/home/omarci/masters/MScDissertation/data/translated_all_descriptions.csv"
detection_filepath = "/home/omarci/masters/MScDissertation/data/lang_all_detection_output.csv"
merged_translated_data_filepath = "/home/omarci/masters/MScDissertation/data/all_descriptions_translated_full.csv"

# Translation lib: https://pypi.org/project/deep-translator/
# Detection (local) lib: https://towardsdatascience.com/introduction-to-googles-compact-language-detector-v3-in-python-b6887101ae47
# gcld3 on PyPi

df = pd.read_csv(merged_data_filepath)
print(f"Number of rows in input: {df.shape[0]}")
print(f"Number of nonexistent job descriptions: {sum(df.unescapedJobDesc.isna())}") # 20
df.dropna(inplace=True, subset=["unescapedJobDesc"])
detectionDf = df[["id", "unescapedJobDesc"]]
translatedDescriptions = pd.DataFrame({"id": [], "translatedJobDesc": []})

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

    Returns:
    translatedText - pd.DataFrame: A pandas DataFrame
    of size batchSize with 2 columns: id and translatedJobDesc
    that each hold a unique identifier and the translated job
    description
    selectedIds - [int]: A list of IDs selected
    """

    outdf = pd.DataFrame()

    # Exclude IDs not needed
    selectiondf = df[~df['id'].isin(excludeIds)]
    
    # Randomly  select batchSize number of IDs
    selectedIds = rnd.sample(selectiondf.id.tolist(), batchSize)

    selectiondf = df[df['id'].isin(selectedIds)]
    outdf["id"] = selectiondf.id
    outdf["translatedJobDesc"] = translate_job_deeptrans(selectiondf.unescapedJobDesc.tolist())
    
    return outdf, selectedIds


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
# Maximum translation can handle is 5000 characters - check how limiting this is...
print(f"Number of job descriptions above 5000 characters: {sum(df.unescapedJobDesc.str.len() >= 5000)}") #209
print(f"Number of job descriptions below 200 characters: {sum(df.unescapedJobDesc.str.len() <= 200)}")
# Can we save them? Seems like a lot are in English?
saveIds = df[df.unescapedJobDesc.str.len() >= 5000].id
# NOTE: Detected English job descriptions are/were NOT translated

if __name__ == "__main__":
    if detectLang:
        detectionDf[['descLanguage', 'languageProb']] = detectionDf.apply(lambda row: pd.Series(detect_language(row, detector)), axis=1)
        detectionDf.to_csv(detection_filepath)

    if translate:
        # Remove jobs with fewer than 200 or more than 5k characters
        print(f"Number of rows in input: {df.shape[0]}")
        longTexts = df[df.unescapedJobDesc.str.len() >= 5000].id # 205
        shortTexts = df[df.unescapedJobDesc.str.len() <= 200].id # 165
        translationDf = df[~(df.id.isin(longTexts) | df.id.isin(shortTexts))]
        print(f"With short ({len(shortTexts)}) and long ({len(longTexts)}) texts removed: {translationDf.shape[0]}")

        # filter jobs that need translation
        englishIds = detectionDf[detectionDf.descLanguage == "en"].id
        translationDf = translationDf[~translationDf.id.isin(englishIds)].copy(deep=True)
        translationDf["unescapedJobDesc"] = translationDf.unescapedJobDesc.str.slice(0, 4999)
        notTranslated = []

        for i in range(int(np.ceil(translationDf.shape[0]/batchSize))):
            try:
                # Translate stuff
                returndf, selectedIds = translate_in_batches(
                    translationDf[["id", "unescapedJobDesc"]],
                    translatedDescriptions.id.tolist(),
                    batchSize=batchSize)

                # Capture results
                translatedDescriptions = pd.concat([translatedDescriptions, returndf])
                translatedDescriptions =  translatedDescriptions[["id", "translatedJobDesc"]]

            except Exception as e:
                print(f"Error occurred: {e}")
                print(f"Row IDs: {selectedIds}")
                notTranslated.append(selectedIds)

            # Wait between tries
            time.sleep(batchSize)

        # Retry missing valuesú
        notTranslated = list(itertools.chain(*notTranslated))
        missingText = df[df.id.isin(notTranslated)].copy(deep=True)
        missingText["unescapedJobDesc"] = missingText.unescapedJobDesc.str.slice(0, 4999)
        try:
            returndf, _ = translate_in_batches(
                        missingText[["id", "unescapedJobDesc"]],
                        [],
                        batchSize=missingText.shape[0])
        except Exception as e:
            print("Retry for translation failed!")

        # Bring in English job descriptions
        engJobDescDf = df[df.id.isin(englishIds)][["id", "unescapedJobDesc"]]
        engJobDescDf.rename(
            columns={"unescapedJobDesc": "translatedJobDesc"},
            inplace=True
        )
        translationDf = pd.concat([engJobDescDf, translatedDescriptions, returndf])
        translationDf.drop_duplicates(subset="id", inplace=True)

        # Bring in original data
        df["id"] = df.id.astype(int)
        translationDf["id"] = translationDf.id.astype(int)
        df = df.merge(translationDf, on=["id"], how="left")
        
        # Save results
        translationDf.to_csv(translations_filepath)

    #Join results together
    if joinResults:
        # df -> 4584
        # languageDf -> 4214 after  165 + 205 extremes removed
        detectionDf = pd.read_csv(detection_filepath)

        df["id"] = df.id.astype(int)
        languageDf = df.merge(detectionDf[["id", "descLanguage", "languageProb"]], on=["id"], how="left")

        # Drop short and long texts from output
        longTexts = df[df.unescapedJobDesc.str.len() >= 5000].id # 205
        shortTexts = df[df.unescapedJobDesc.str.len() <= 200].id # 165
        languageDf = languageDf[~(languageDf.id.isin(longTexts) | languageDf.id.isin(shortTexts))]

        # Summary stats about language
        print(f"Language counts: {languageDf.descLanguage.value_counts()}")
        # 60% Hungarian, 30% English, 5% German - 5% Other
        # (Other: lithuanian, polish, russian, ukrainian, romanian, french)
        languageDf.languageProb.describe()
        # Predictor is confident: 5 values below 50% probability

        # Check detection for English - probability
        engDf = languageDf[languageDf.descLanguage == "en"]
        engDf.languageProb.describe()
        unsureDf = engDf[engDf.languageProb < 0.9]
        # Manual inspection: Mostly IT roles with full English description
        # other than location and company name which confuses algorithm IMO

        # Check detection probability a bit more
        unsureDf = languageDf[languageDf.languageProb < 0.9]
        # Other jobs (not categorized as English) have LOTs of English
        # stuff in them (such as work technologies) but also
        # most of the description body is in foreign language

        print(f"Number of rows in output: {languageDf.shape[0]}")
        # Save results
        languageDf.to_csv(merged_translated_data_filepath, encoding='utf-8')

    a = 1