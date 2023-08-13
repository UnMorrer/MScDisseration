# Other than InfoShield, do I have other clustering methods available?
# NOTE: https://scikit-learn.org/stable/modules/clustering.html - reliable description of many tools + Word doc
import pandas as pd
import sklearn
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from cycler import cycler

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
hatch_cycle = (cycler('hatch', ['///', '||', '--', '...','\///', 'xxx', '\\\\']))
styles = hatch_cycle()


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

def assign_label(value):
    """
    Function to assign clusters into groups by size
    """
    if value == 2:
        return '2'
    elif value == 3:
        return '3'
    elif value == 4:
        return '4'
    elif value >= 5 and value <= 9:
        return '5-9'
    elif value >= 10 and value <= 19:
        return '10-19'
    elif value >= 20:
        return '20+'

labelOrder = ["2", "3", "4", "5-9", "10-19", "20+"]

for version in range(1, 5, 1):
    clusters = f"/home/omarci/masters/MScDissertation/InfoShield/infoshield{version}_full_LSH_labels.csv"
    clusters = pd.read_csv(clusters, usecols=["LSH label", "id"])
    clusters = clusters.merge(data, how="inner", on="id")
    size = clusters.groupby("LSH label")["totalIndicators"].count().drop(index=-1)

    diff = within_cluster_dispersion(clusters, power=1)
    var = within_cluster_dispersion(clusters, power=2)
    print("-"*20)
    print(f"Version {version} \n")
    print(f"Within-cluster differences: {diff.drop(index=-1).sum()[0]} ({diff.sum()[0]})")
    print(f"Within-cluster variance: {var.drop(index=-1).sum()[0]} ({var.sum()[0]})")
    print("-"*20)

    # Plot histogram of cluster sizes
    plt.clf()
    plt.hist(x=size.values, log=True, color="0.85", bins=range(2,max(size.values)+1, 1), edgecolor="black")
    plt.grid(which='major', axis='y', linestyle='--', linewidth=0.5, color='gray')
    # Align plots so they are comparable just by a brief look
    plt.xlim((1,55))
    plt.xlabel("Adverts in cluster")
    plt.ylabel("Number of clusters (log scale)")
    plt.title(f"Number of clusters and cluster size - Method {version}")
    plt.savefig(f"/home/omarci/masters/MScDissertation/figures/clusters/clusterSize{version}.png")

    # Plot mean difference/variance (within cluster) by cluster size
    # Question: Do smaller clusters approximate better?
    # Groups: 2, 3, 4, 5-9, 10-19, 20+
    df = size.reset_index().rename(columns={"totalIndicators":"clusterSize"})
    df["clusterGroup"] = df["clusterSize"].apply(assign_label)
    df = df.merge(diff.reset_index().rename(columns={"dispersion":"diff"}), on="LSH label", how="inner")
    df = df.merge(var.reset_index().rename(columns={"dispersion":"var"}), on="LSH label", how="inner")
    df["avgDiff"] = df["diff"]/df["clusterSize"]
    df["avgVar"] = df["var"]/df["clusterSize"]

    weighted_mean = lambda x: np.average(x, weights=df.loc[x.index, "clusterSize"])

    varGraph = df.groupby("clusterGroup").agg(weightedMean=("avgVar", weighted_mean))
    diffGraph = df.groupby("clusterGroup").agg(weightedMean=("avgDiff", weighted_mean))

    # Reorder index
    diffGraph = diffGraph.loc[labelOrder]
    varGraph = varGraph.loc[labelOrder]

    # Create graphs for mean difference in cluster
    plt.clf()
    plot = sns.barplot(y=diffGraph.weightedMean, x=diffGraph.index, color="white", edgecolor="black", linewidth=2)
    for i, bar in enumerate(plot.patches):
        bar.set_hatch(**next(styles))
    plt.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='gray')
    plt.xlabel("Cluster size")
    plt.ylabel("Mean difference")
    plt.ylim((0, 1)) # Make graphs comparable
    plt.title(f"Mean difference from centroid by cluster size \nMethod {version}")
    plt.tight_layout()
    plt.savefig(f"/home/omarci/masters/MScDissertation/figures/clusters/meanDiff{version}.png")

    # Create graphs for mean /variance in cluster
    plt.clf()
    plot = sns.barplot(y=varGraph.weightedMean, x=varGraph.index, color="white", edgecolor="black", linewidth=2)
    for i, bar in enumerate(plot.patches):
        bar.set_hatch(**next(styles))
    plt.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='gray')
    plt.xlabel("Cluster size")
    plt.ylabel("Mean variance")
    plt.ylim((0, 0.5)) # Make graphs comparable
    plt.title(f"Mean variance from centroid by cluster size \nMethod {version}")
    plt.tight_layout()
    plt.savefig(f"/home/omarci/masters/MScDissertation/figures/clusters/meanVar{version}.png")


a = 1