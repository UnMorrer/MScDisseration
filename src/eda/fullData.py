# Exploratory data analysis for jobs with full data
# - Language - deepl module
# - Salary
# - Country
# - Duplicate ads with cosine similarity
# - etc.

import pandas as pd
import configparser
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Read in data
df = pd.read_csv("/home/omarci/masters/MScDissertation/data/merged_full.csv")
config = configparser.ConfigParser()
config.read(".env")

# Character number in full description
print(f"Summary stats - number of characters in job description: \n")
print(df.jobDescription.str.len().describe())
# Min 25 - Max 14,542: Enormous range present BUT all below 15k character limit for translation

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

# Examine countries and salary data
print(f"NO salary recorded for {sum(df.salary.isna())}/{df.shape[0]} observations")
print(f"Country breakdown: {df.locationName.value_counts()}")
# Generic abroad for 1706/4878 countries