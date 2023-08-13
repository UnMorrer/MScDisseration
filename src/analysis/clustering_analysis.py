# Other than InfoShield, do I have other clustering methods available?
# NOTE: https://scikit-learn.org/stable/modules/clustering.html - reliable description of many tools + Word doc
import pandas as pd
import sklearn
import numpy as np

bootstrap = True # Treu results in significantly more calculations!
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
indicatorList = [ # Indicators used for analysis etc.
    "indTransportToWork",
    "indAccommodationProvided",
    "indSharedAccommodation",
    "indTransferAbroad",
    "indHelpAdministration",
    "indWorkingHours",
    "indWage", 
    "indLocalLanguage", 
    "indWageDeduction", 
    "indNoExperience"
]
data = pd.read_csv(data, usecols=(list(dataTypes.keys()) + extraCols), dtype=dataTypes, parse_dates=["date"])

# Fill NA with zeros and convert to integers for downstream calculations
for indicator in indicatorList:
    data[indicator] = data[indicator].fillna(0).astype(int).copy()

# NOTE: For bootstrap purposes, examine using InfoShield-coarse ONLY
#   YES - full results and coarse results identical
# NOTE: InfoShield is deterministic - bootstrap the ads present
##########################################
# Evaluation functions
##########################################

# Cluster homogeneity
# Within-cluster dispersion matrix from Variance Ratio criterion
def within_cluster_dispersion(data, usevars=indicatorList, label="LSH label", power=2):
    """
    Function to calculate within-cluster dispersion
    Formula: https://scikit-learn.org/stable/modules/clustering.html#clustering-performance-evaluation
    2.3.11.6 W_k - Within-cluster dispersion

    Inputs:
    data - pd.DataFrame: Dataframe that contains
    the data for the analysis
    usevars - [str]: List of column names
    in data that are used to calculate dispersion metric
    label - str: Column name in dataframe that contains
    label assignment
    power - int: Controls dispersion metric. Power=2
    calculates variance while power=1 calculates
    (raw) differences.

    Returns:
    dispersion - pd.Series: Series that contains
    the calculated dispersion for each cluster.
    Sum up to obtain values for the entire dataset
    """
    df = data[usevars+[label]].copy()

    # Calculate centroid locations for each cluster
    centroids = df.groupby(label).mean()

    # Apply dispersion calculation for each row/observation
    df["dispersion"] = df.apply(lambda row: np.sum(np.abs(row[usevars] - centroids.loc[row[label]])**power), axis=1)

    return df[[label, "dispersion"]].groupby(label).sum()

##########################################
# Loop evaluation
##########################################

for version in range(1, 5, 1):
    clusters = f"/home/omarci/masters/MScDissertation/InfoShield/infoshield{version}_full_LSH_labels.csv"
    clusters = pd.read_csv(clusters, usecols=["LSH label", "id"])
    clusters = clusters.merge(data, how="inner", on="id")

    diff = within_cluster_dispersion(clusters, power=1)
    var = within_cluster_dispersion(clusters, power=2)
    print("-"*20)
    print(f"Version {version} \n")
    print(f"Within-cluster differences: {diff.drop(index=-1).sum()} ({diff.sum()})")
    print(f"Within-cluster variance: {var.drop(index=-1).sum()} ({var.sum()})")
    print("-"*20)

# TODO: Density plots for cluster-level differences

a = 1