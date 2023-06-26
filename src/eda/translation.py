import deep_translator as dptrans

# TODO: Look into LOCAL translation, or at least language detection
# Translation lib: https://pypi.org/project/deep-translator/
# Detection (local) lib: https://towardsdatascience.com/develop-a-text-language-detector-and-translator-system-in-python-6537d6244b10
# --> Module: cld3 - https://github.com/google/cld3

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

