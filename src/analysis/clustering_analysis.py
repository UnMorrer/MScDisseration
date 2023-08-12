# How can I identify significant variables in clustering?
# Variables that "define" clusters -> low intra-cluster variance and high inter-cluster variance
# adjusted rand index???

# Other than InfoShield, do I have other clustering methods available?

# + research q: what is the best way to cluster? Native text, translated text or something completely different?
import pandas as pd

data = "/home/omarci/masters/MScDissertation/data/final_dataset.csv"
clusters = "/home/omarci/masters/MScDissertation/InfoShield/infoshield1_full_LSH_labels.csv"
dataTypes = {
    "id": int,
    "destCountry": str,
    "unescapedJobDesc": str,
    "translatedJobDesc": str,
    "descLanguage": str,
    "indTransportToWork": bool,
    "indAccommodationProvided": bool,
    "indSharedAccommodation": bool,
    "indTransferAbroad": bool,
    "indHelpAdministration": bool,
    "totalIndicators": int,
    # Additional stuff - might not be needed AT ALL
    "industrySector": str,
    "jobNature": str,
    "contractType": str,
    "genderRequirements": str,
    "ageRequirements": str,
    "accommodationPaidByWorker": str,
    "urgentDeparture": str,
    "overtimeOffered": str,
    "socialBenefits": str,
}
# Columns where no data types can be specified
extraCols = ["date", "indWorkingHours", "indWage", "indLocalLanguage", "indWageDeduction", "indNoExperience"]
data = pd.read_csv(data, usecols=(list(dataTypes.keys()) + extraCols), dtype=dataTypes, parse_dates=["date"])
clusters = pd.read_csv(clusters, usecols=["LSH label", "id"])

data = clusters.merge(data, how="inner", on="id")

# Brainstorming:
# Dimensionality reduction?

# Silhouette analysis
# Davies-Bouldin index
# Calinski-Harabasz Index (Variance Ratio Criterion)
# Dunn Index
# ANOVA - Normality assumption! -> Kruskal-Wallis Test
# Chi-squared test
# Cramer's V
# Multidimensional Scaling
# Principal Component Analysis
# Jaccard Index
# Entropy (within-cluster homogeneity)
# Hamming Distance
# Gini index

# For totals:
# Mean - standard deviation within/across clusters (cluster averages)
# 
a = 1