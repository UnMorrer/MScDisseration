# TODO: Bootstrap for InfoShield
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
fullSamples = []
foreignSamples = []
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
# Columns where no data types can be specified
extraCols = ["indWorkingHours", "indWage", "indLocalLanguage", "indWageDeduction", "indNoExperience"]

data = pd.read_csv(data, usecols=(list(dataTypes.keys()) + extraCols), dtype=dataTypes)
foreignData = data[~data["destCountry"].isin(["hungary", "not specified"])].copy()

# Sample IDs
for _ in range(bootstrapSamples):
    # Sample with replacement from the DataFrame
    sample = data.sample(n=len(data), replace=True)
    fullSamples.append(sample)
    sample = foreignData.sample(n=len(foreignData), replace=True)
    foreignSamples.append(sample)

# Run clustering on samples
    coarse = ic.InfoShieldCoarse(*sys.argv[1:])
    coarse.clustering()
    labels = coarse.labels

# Calculate mean error and mean squared error statistics

a = 1