# Other than InfoShield, do I have other clustering methods available?
# NOTE: https://scikit-learn.org/stable/modules/clustering.html - reliable description of many tools + Word doc
# NOTE: highest possible Mean Aboslute Error is 5 -> 10*0.5 (if cluster centroid is at 0.5)
# TODO: Is the disagreement (cluster mean abs error) specific to some indicators or is it widespread (within clusters)?
# TODO: Capture data from last comparison to table in dissertation???
# TODO: Add confidence intervals for cluster errors (using bootstrap)
import pandas as pd
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from cycler import cycler
import utils.calc_cluster_errors as cce
import itertools

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


##########################################
# Loop evaluation
##########################################

labelOrder = ["2", "3", "4", "5-9", "10-19", "20+"]

for version in range(1, 5, 1):
    clusters = f"/home/omarci/masters/MScDissertation/InfoShield/infoshield{version}_full_LSH_labels.csv"
    clusters = pd.read_csv(clusters, usecols=["LSH label", "id"])
    clusters = clusters.merge(data, how="inner", on="id")
    size = clusters.groupby("LSH label")["totalIndicators"].count().drop(index=-1)

    diff = cce.within_cluster_dispersion(data=clusters, usevars=indicatorList, label="LSH label", power=1)
    # var = cce.within_cluster_dispersion(data=clusters, usevars=indicatorList, label="LSH label", power=2)
    print("-"*20)
    print(f"Version {version} \n")
    print(f"Within-cluster differences: {diff.drop(index=-1).sum()[0]} ({diff.sum()[0]})")
    # print(f"Within-cluster variance: {var.drop(index=-1).sum()[0]} ({var.sum()[0]})")
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
    df["clusterGroup"] = df["clusterSize"].apply(cce.assign_label)
    df = df.merge(diff.reset_index().rename(columns={"dispersion":"diff"}), on="LSH label", how="inner")
    # df = df.merge(var.reset_index().rename(columns={"dispersion":"var"}), on="LSH label", how="inner")
    df["avgDiff"] = df["diff"]/df["clusterSize"]
    # df["avgVar"] = df["var"]/df["clusterSize"]

    weighted_mean = lambda x: np.average(x, weights=df.loc[x.index, "clusterSize"])

    # varGraph = df.groupby("clusterGroup").agg(weightedMean=("avgVar", weighted_mean))
    diffGraph = df.groupby("clusterGroup").agg(weightedMean=("avgDiff", weighted_mean))

    # Reorder index
    diffGraph = diffGraph.loc[labelOrder]
    #varGraph = varGraph.loc[labelOrder]

    # Create graphs for mean difference in cluster
    plt.clf()
    plot = sns.barplot(y=diffGraph.weightedMean, x=diffGraph.index, color="white", edgecolor="black", linewidth=2)
    for i, bar in enumerate(plot.patches):
        bar.set_hatch(**next(styles))
    plt.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='gray')
    plt.xlabel("Cluster size")
    plt.ylabel("Mean error")
    plt.ylim((0, 1)) # Make graphs comparable
    plt.title(f"Mean error by cluster size \nMethod {version}")
    plt.tight_layout()
    plt.savefig(f"/home/omarci/masters/MScDissertation/figures/clusters/meanError{version}.png")

    ##########################################
    # Distribution of avgDiff in cluster groups
    ##########################################
    for clusterGroup in labelOrder:
        histGraph = df[df.clusterGroup == clusterGroup].avgDiff

        # Plot histogram of mean error within cluster
        plt.clf()
        plt.hist(x=histGraph.values, bins=np.arange(0, 1.5, 0.1),color="0.85", edgecolor="black")
        plt.grid(which='major', axis='y', linestyle='--', linewidth=0.5, color='gray')
        # Align plots so they are comparable just by a brief look
        plt.xlabel("Mean error for cluster")
        plt.ylabel("Number of clusters")
        plt.title(f"Mean error in clusters \n Method {version} | Cluster size {clusterGroup}")
        plt.savefig(f"/home/omarci/masters/MScDissertation/figures/clusters/meanErrorHistogram{version}Cluster{clusterGroup}.png")

    # Create graphs for mean /variance in cluster
    # plt.clf()
    # plot = sns.barplot(y=varGraph.weightedMean, x=varGraph.index, color="white", edgecolor="black", linewidth=2)
    # for i, bar in enumerate(plot.patches):
    #     bar.set_hatch(**next(styles))
    # plt.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='gray')
    # plt.xlabel("Cluster size")
    # plt.ylabel("Mean squared error")
    # plt.ylim((0, 0.5)) # Make graphs comparable
    # plt.title(f"Mean squared error by cluster size \nMethod {version}")
    # plt.tight_layout()
    # plt.savefig(f"/home/omarci/masters/MScDissertation/figures/clusters/meanSqError{version}.png")

##########################################
# Compare different methods to each other
##########################################

# Adjusted Rand Index
# Adjusted Mutual Information
# Fowlkes-Mallows Index

clusterResults = {
    1: pd.read_csv("/home/omarci/masters/MScDissertation/InfoShield/infoshield1_full_LSH_labels.csv", usecols=["LSH label", "id"]).sort_values(by="id"),
    2: pd.read_csv("/home/omarci/masters/MScDissertation/InfoShield/infoshield2_full_LSH_labels.csv", usecols=["LSH label", "id"]).sort_values(by="id"),
    3: pd.read_csv("/home/omarci/masters/MScDissertation/InfoShield/infoshield3_full_LSH_labels.csv", usecols=["LSH label", "id"]).sort_values(by="id"),
    4: pd.read_csv("/home/omarci/masters/MScDissertation/InfoShield/infoshield4_full_LSH_labels.csv", usecols=["LSH label", "id"]).sort_values(by="id"),
}

for comparison in list(itertools.combinations(clusterResults.keys(), 2)):
    print("-"*20)
    print(f"Comparison between method {comparison[0]} and method {comparison[1]}")

    # Align IDs
    data1 = clusterResults[comparison[0]]
    data2 = clusterResults[comparison[1]]
    data = data1.merge(data2, how="inner", on="id", suffixes=(" 1", " 2"))
    print(f"Number of rows in comparison: {data.shape[0]}")
    labels1 = data["LSH label 1"].tolist()
    labels2 = data["LSH label 2"].tolist()

    # Calculate similarity metrics
    rand = metrics.adjusted_rand_score(labels1, labels2)
    ami = metrics.adjusted_mutual_info_score(labels1, labels2)
    fmi = metrics.fowlkes_mallows_score(labels1, labels2)

    print(f"Adjusted rand index: {rand:.5f}")
    print(f"Adjusted mutual information: {ami:.5f}")
    print(f"Fowlkes-Mallows index: {fmi:.5f}")

a = 1