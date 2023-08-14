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

data = pd.read_csv(data, usecols=(list(dataTypes.keys()) + extraCols), dtype=dataTypes)
foreignData = data[~data["destCountry"].isin(["hungary", "not specified"])].copy()

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

        coarse = ic.InfoShieldCoarse(data=sample[["id", "unescapedJobDesc"]], doc_id_header="id", doc_text_header="unescapedJobDesc")
        coarse.clustering()
        # Calculate mean error and mean squared error statistics
        df = sample.copy(deep=True)[indicatorList + ["id"]].fillna(0).astype(int)
        df["label"] = coarse.labels
        df["round"] = i
        diff = cce.within_cluster_dispersion(data=df, usevars=indicatorList, label="label", power=1).drop(index=-1).sum()[0]
        var = cce.within_cluster_dispersion(data=df, usevars=indicatorList, label="label", power=2).drop(index=-1).sum()[0]
        stat.append([diff, var, i])
        label.append(df[["id", "label", "round"]])

# Save results - Tested working
basePath = "/home/omarci/masters/MScDissertation/data/"
for label, stat, j in zip(labels, stats, methodTracker):
    df = pd.concat(label, axis=0, ignore_index=True)
    df.to_csv(f"{basePath}bootstrapLabels_Method{j}.csv", encoding='utf-8-sig')

    statDf = pd.DataFrame(data=stat, columns=["meanError", "meanSqError", "round"])
    statDf.to_csv(f"{basePath}bootstrapStats_Method{j}.csv", encoding='utf-8-sig')

# Turn off PC when done - NOTE: Maybe remove later
os.system("shutdown /s /t 60")