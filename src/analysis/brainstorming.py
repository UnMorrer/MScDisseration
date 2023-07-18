# InfoShield clustering - OK
# Correlates collected - OK

# How can I identify significant variables in clustering?
# Variables that "define" clusters -> low intra-cluster variance and high inter-cluster variance
# adjusted rand index???

# Other than InfoShield, do I have other clustering methods available?
import pandas as pd

translatedDf = pd.read_csv("/home/omarci/masters/MScDisseration/data/merged_translated_full.csv")

# InfoShield - 3 interesting clustering methods
# 1 -> unescaped text, all job adverts
# 2 -> unescaped text, selected job adverts
# 3 -> translated text, selected job adverts

a = 1

# outDf.to_csv("/home/omarci/masters/MScDisseration/data/merged_translated_full.csv") # -> 4206 recordstrans