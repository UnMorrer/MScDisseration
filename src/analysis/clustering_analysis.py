# Other than InfoShield, do I have other clustering methods available?
# NOTE: https://scikit-learn.org/stable/modules/clustering.html - reliable description of many tools + Word doc
# NOTE: highest possible Mean Aboslute Error is 5 -> 10*0.5 (if cluster centroid is at 0.5)
# TODO: Capture data from last comparison to table in dissertation???
import pandas as pd
from sklearn import metrics
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from cycler import cycler
import utils.calc_cluster_errors as cce
import itertools

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
indicatorCols = {
    "indWorkingHours": "Working hours above legal limit",
    "indWage" : "Wage below national minimum",
    "indLocalLanguage" : "Local language not required",
    "indTransportToWork" : "Transport to work provided",
    "indAccommodationProvided" : "Accommodation provided",
    "indSharedAccommodation" : "Shared accommodation",
    "indWageDeduction" : "Deduction from wages",
    "indTransferAbroad" : "Transfer abroad provided",
    "indNoExperience" : "No prior experience required",
    "indHelpAdministration" : "Help with administration"
}

for version in range(1, 5, 1):
    clusters = f"/home/omarci/masters/MScDissertation/InfoShield/infoshield{version}_full_LSH_labels.csv"
    bootstrap = f"/home/omarci/masters/MScDissertation/data/bootstrapStats_Method{version}.csv"
    bootstrap = pd.read_csv(bootstrap)
    clusters = pd.read_csv(clusters, usecols=["LSH label", "id"])
    clusters = clusters.merge(data, how="inner", on="id")
    size = clusters.groupby("LSH label")["totalIndicators"].count().drop(index=-1)

    diff = cce.within_cluster_dispersion(data=clusters, usevars=indicatorList, label="LSH label", power=1)
    # var = cce.within_cluster_dispersion(data=clusters, usevars=indicatorList, label="LSH label", power=2)
    print("-"*20)
    print(f"Version {version} \n")
    print(f"Mean absolute error for all clusters: {diff.drop(index=-1).sum()[0]} ({diff.sum()[0]})")
    numClusters = len(clusters['LSH label'].unique()) - 1
    print(f"Number of cluster for method {version}: {numClusters}")
    print(f"Number of ads within clusters: {clusters[clusters['LSH label'] != -1].shape[0]}")
    # print(f"Within-cluster variance: {var.drop(index=-1).sum()[0]} ({var.sum()[0]})")

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
    twoObservations = size.value_counts().iloc[0]
    print(f"Number of clusters with size 2 for method {version}: {twoObservations} ({twoObservations / numClusters * 100}%)")

    # Plot mean difference/variance (within cluster) by cluster size
    # Question: Do smaller clusters approximate better?
    # Groups: 2, 3, 4, 5-9, 10-19, 20+
    diffGraph = cce.calculate_grouped_results(size.reset_index().rename(columns={"totalIndicators":"clusterSize"}), diff)

    # Get 95% CI using 5 - 95th largest bootstrap estimates
    # ci = bootstrap.quantile([0.05, 0.95], axis=0)
    # lower = ci.iloc[0, :][["2", "3", "4", "5-9", "10-19", "20+"]].to_numpy()
    # upper = ci.iloc[1, :][["2", "3", "4", "5-9", "10-19", "20+"]].to_numpy()
    # lowerError = (diffGraph.to_numpy()[:, 0] - lower).clip(0)
    # upperError = (upper - diffGraph.to_numpy()[:, 0]).clip(0)

    # Create graphs for mean difference in cluster
    print(f"Mean abs error for cluster size 20+: {diffGraph.weightedMean.iloc[5]:.3f}")
    print(f"Mean abs error for cluster size 10-19: {diffGraph.weightedMean.iloc[4]:.3f}")
    print(f"Mean abs error for cluster size 5-9: {diffGraph.weightedMean.iloc[3]:.3f}")
    plt.clf()
    plot = sns.barplot(y=diffGraph.weightedMean, x=diffGraph.clusterGroup, color="white", edgecolor="black", linewidth=2)#, yerr=[lowerError, upperError])
    for i, bar in enumerate(plot.patches):
        bar.set_hatch(**next(styles))
    plt.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='gray')
    plt.xlabel("Cluster size")
    plt.ylabel("Mean abs error per advert")
    plt.ylim((0, 1)) # Make graphs comparable
    plt.title(f"Mean absolute error by cluster size \nMethod {version}")
    plt.tight_layout()
    plt.savefig(f"/home/omarci/masters/MScDissertation/figures/clusters/meanError{version}.png")

    # Mean absolute error calculation per indicator per clusterGroup
    clusterBreakdown = []
    for indicator in indicatorList:
        result = cce.within_cluster_dispersion(data=clusters, usevars=[indicator], label="LSH label", power=1)
        groupedResult = cce.calculate_grouped_results(size.reset_index().rename(columns={"totalIndicators":"clusterSize"}), result)
        clusterBreakdown.append([version, indicator, *groupedResult.weightedMean.to_list()])
    
    clusterBreakdown = pd.DataFrame(data=clusterBreakdown, columns=["method", "indicatorName", *labelOrder])
    # Convert to percentages + stacked barplot
    percentages = clusterBreakdown[labelOrder].div(clusterBreakdown[labelOrder].sum(axis=0), axis=1)*100
    percentages.set_index(clusterBreakdown.indicatorName, inplace=True)

    plt.clf()
    fig, ax = plt.subplots()
    bottom = np.zeros(len(labelOrder))

    for row in percentages.iterrows():
        p = ax.bar(
            labelOrder,
            row[1].to_numpy(),
            label=indicatorCols[row[0]],
            bottom=bottom)
        bottom += row[1].to_numpy()

    ax.set_title(f"Breakdown of mean absolute error \n  Method {version}")
    plt.ylabel("Percentage of cluster-level errors")
    plt.xlabel("Cluster size")
    # ax.legend(loc="upper right")
    # plt.legend(bbox_to_anchor=(1, 0.40), loc="lower left") - moved to separate picture
    plt.grid(which='major', axis='y', linestyle='--', linewidth=0.5, color='gray')
    plt.savefig(f"/home/omarci/masters/MScDissertation/figures/clusters/errorBreakdown{version}.png", bbox_inches="tight")

    ##########################################
    # Distribution of avgDiff in cluster groups
    ##########################################
    histGraph = diff.merge(size, on="LSH label").rename(columns={"totalIndicators": "clusterSize"})
    histGraph["clusterGroup"] = histGraph.clusterSize.apply(cce.assign_label)
    histGraph["error"] = histGraph.dispersion / histGraph.clusterSize
    for clusterGroup in labelOrder:
        graphData = histGraph[histGraph.clusterGroup == clusterGroup]
        # Plot histogram of mean error within cluster
        plt.clf()
        plt.hist(x=graphData.error, bins=np.arange(0, 1.2, 0.1),color="0.85", edgecolor="black")
        plt.grid(which='major', axis='y', linestyle='--', linewidth=0.5, color='gray')
        # Align plots so they are comparable just by a brief look
        plt.xlabel("Mean abs error within cluster")
        plt.ylabel("Number of clusters")
        plt.ylim((0, 7))
        plt.title(f"Mean absolute error distribution for clusters \n Method {version} | Cluster size {clusterGroup}")
        plt.savefig(f"/home/omarci/masters/MScDissertation/figures/clusters/meanErrorHistogram{version}Cluster{clusterGroup}.png")
    
    print("-"*20)

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

# Example clusters
data = "/home/omarci/masters/MScDissertation/data/final_dataset.csv"
data = pd.read_csv(data, usecols=(list(dataTypes.keys()) + extraCols), dtype=dataTypes, parse_dates=["date"])
clusters = f"/home/omarci/masters/MScDissertation/InfoShield/infoshield2_full_LSH_labels.csv"
clusters = pd.read_csv(clusters, usecols=["LSH label", "id"])
clusters = clusters.merge(data, how="inner", on="id")

# Small adverts in cluster
clusters = clusters[clusters["LSH label"] != -1].copy()
smallAds = clusters[clusters.translatedJobDesc.str.len() <= 400]
smallAds["LSH label"].value_counts()
examples = smallAds[smallAds["LSH label"] == 65].id.values
# ID 73, 1064 will be included
a = 1