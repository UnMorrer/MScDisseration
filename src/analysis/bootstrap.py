# Bootstrap for InfoShield
# 100 iterations for all 4 methods for starters
# Infoshield-coarse is perfectly fine
# Compare variance/difference to original
# AND utilize other methods (see doc) - original as "ground truth" label
# Different ads -> cannot compare labels directly. Needs to deduce set with unique IDs and their labels
# Kinda useless stat but why not = are all duplicate ads in the same cluster?

import pandas as pd
import utils.infoshieldcoarse as ic
import utils.calc_cluster_errors as cce
import os
import numpy as np

bootstrapSamples = 100
labels = [[], [], [], []]
stats = [[], [], [], []]
methodTracker = [1, 2, 3, 4]
data = "/home/omarci/masters/MScDissertation/data/final_dataset.csv"
dataTypes = {
    "id": int,
    "destCountry": str,
    "unescapedJobDesc": str,
    "translatedJobDesc": str,
    "indTransportToWork": bool,
    "indAccommodationProvided": bool,
    "indSharedAccommodation": bool,
    "indTransferAbroad": bool,
    "indHelpAdministration": bool,
    "totalIndicators": int,
}
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
# Columns where no data types can be specified
extraCols = ["indWorkingHours", "indWage", "indLocalLanguage", "indWageDeduction", "indNoExperience"]
labelOrder = ["2", "3", "4", "5-9", "10-19", "20+"]

data = pd.read_csv(data, usecols=(list(dataTypes.keys()) + extraCols), dtype=dataTypes)
foreignData = (data["destCountry"] == "hungary") | (data["destCountry"].isna())
foreignData = data[~foreignData].copy() # 1811 rows

# Sample IDs
for i in range(bootstrapSamples):
    # Sample with replacement from the DataFrame
    sample12 = data.sample(n=len(data), replace=True)
    sample34 = foreignData.sample(n=len(foreignData), replace=True)
    for label, stat, j in zip(labels, stats, methodTracker):
        # Run clustering on samples
        # Method 1
        if j < 3:
            sample = sample12
        else:
            sample = sample34

        if j % 2 == 0:
            textCol = "translatedJobDesc"
        else:
            textCol = "unescapedJobDesc"

        coarse = ic.InfoShieldCoarse(data=sample[["id", textCol]], doc_id_header="id", doc_text_header=textCol)
        coarse.clustering()
        # Calculate mean error and mean squared error statistics
        df = sample.copy(deep=True)[indicatorList + ["id"]].fillna(0).astype(int).copy()
        df["label"] = coarse.labels
        df["round"] = i
        diff = cce.within_cluster_dispersion(data=df, usevars=indicatorList, label="label", power=1)
        diffSum = diff.drop(index=-1).sum()[0]

        # Calculate mean absolute error for different cluster groups
        size = df.groupby("label")["id"].count().drop(index=-1)

        df2 = size.reset_index().rename(columns={"id":"clusterSize"})
        df2["clusterGroup"] = df2["clusterSize"].apply(cce.assign_label)
        df2 = df2.merge(diff.reset_index().rename(columns={"dispersion":"diff"}), on="label", how="inner")
        df2["avgDiff"] = df2["diff"]/df2["clusterSize"]
        weighted_mean = lambda x: np.average(x, weights=df2.loc[x.index, "clusterSize"])
        diffGraph = df2.groupby("clusterGroup").agg(weightedMean=("avgDiff", weighted_mean))

        # Reorder index
        diffGraph = diffGraph.reindex(labelOrder).fillna(0)

        stat.append([diffSum, *diffGraph.weightedMean.to_list(), i])
        label.append(df[["id", "label", "round"]])

        print(f"Sample {i} method {j} done")

# Save results - Tested working
basePath = "/home/omarci/masters/MScDissertation/data/"
for label, stat, j in zip(labels, stats, methodTracker):
    df = pd.concat(label, axis=0, ignore_index=True)
    df.to_csv(f"{basePath}bootstrapLabels_Method{j}.csv", encoding='utf-8-sig')

    statDf = pd.DataFrame(data=stat, columns=["meanError", *labelOrder, "round"])
    statDf.to_csv(f"{basePath}bootstrapStats_Method{j}.csv", encoding='utf-8-sig')