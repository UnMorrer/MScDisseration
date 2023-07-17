# InfoShield clustering - OK
# Correlates collected - OK

# How can I identify significant variables in clustering?
# Variables that "define" clusters -> low intra-cluster variance and high inter-cluster variance

# Other than InfoShield, do we have other clustering methods available?
import pandas as pd

translatedDf = pd.read_csv("/home/omarci/masters/MScDisseration/data/merged_translated_full.csv")

a = 1

# outDf.to_csv("/home/omarci/masters/MScDisseration/data/merged_translated_full.csv") # -> 4206 recordstrans