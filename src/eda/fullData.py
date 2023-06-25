# Exploratory data analysis for jobs with full data
# - Language - deepl module
# - Salary
# - Country
# - Duplicate ads with cosine similarity
# - etc.

import pandas as pd
import deepl
import configparser
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

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
# Cosine similarity
# Clustering with InfoShield - language indep. -> on its way

def calculate_cosine_similarity(texts):
    """
    Function that calculates cosine similarity of input texts

    Inputs:
    text - [str]: A list of texts to analyze
    It has n elements

    Returns:
    cos_sim - matrix[int, n x n]: An n x n matrix
    of cosine similarities between the texts
    """

    # Initialize tf-idf matrix
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)

    # Calculate the cosine similarity vector
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return cosine_sim

# sum(df.unescapedJobDesc.isna()) -> 20
# series = df.unescapedJobDesc.isna()
# indices = series[series].index
df.dropna(subset=["unescapedJobDesc"], inplace=True)
cos_sim = calculate_cosine_similarity(df.unescapedJobDesc.tolist())

# calculate some summary statistics
print(f"Summary statistics for cosine similarity: {np.percentile(cos_sim, range(0,100,10))}")
# Finding really similar ads:
threshold = 0.9
similar_ads = np.where((cos_sim > threshold) & (cos_sim < 0.99))
print(f"Ad pairs with higher than {threshold} similarity: {len(similar_ads[0]/2)}")
print(f"This is {len(similar_ads[0])/df.shape[0]**2}% of total pairs.")

# Save output to image
plt.imshow(cos_sim, cmap='Blues', vmin=0, vmax=1)
plt.colorbar()
plt.savefig('figures/cos_sim.png', dpi=300, bbox_inches='tight')

a = 1

# TODO: Examine countries and salary data

# TODO: FIgure out a way to visualize the InfoShield results
# /show them in a meaningful way in the paper

# TODO: Look into LOCAL translation, or at least language detection
# Translation lib: https://pypi.org/project/deep-translator/
# Detection (local) lib: https://towardsdatascience.com/develop-a-text-language-detector-and-translator-system-in-python-6537d6244b10
# --> Module: cld3 - https://github.com/google/cld3