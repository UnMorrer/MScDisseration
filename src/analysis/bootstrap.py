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

bootstrapSamples = 100
labels = [[], [], [], []]
stats = [[], [], [], []]
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
    for label, stat in zip(labels, stats):
        # Run clustering on samples
        # Method 1
        coarse = ic.InfoShieldCoarse(data=sample[["id", "unescapedJobDesc"]], doc_id_header="id", doc_text_header="unescapedJobDesc")
        coarse.clustering()
        # Calculate mean error and mean squared error statistics
        df = sample.copy(deep=True)
        df["label"] = coarse1.labels
        diff = cce.within_cluster_dispersion(data=df, usevars=indicatorList, label="label", power=1).drop(index=-1).sum()[0]
        var = cce.within_cluster_dispersion(data=df, usevars=indicatorList, label="label", power=2).drop(index=-1).sum()[0]
        stats1.append([diff, var])
        df["label"] = coarse.labels
        label.append(df[["id", "label"]])

    b = 2
a = 1