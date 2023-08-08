import pandas as pd

# InfoShield - 3 interesting clustering methods
# 1 -> unescaped text, all job adverts
infoshield1full = pd.read_csv("/home/omarci/masters/MScDissertation/InfoShield/all_descriptions_translated_full_full_LSH_labels.csv")
# 287 + 1 clusters
# 4424 not assigned to cluster

# 2 -> unescaped text, selected job adverts
infoshield2full = pd.read_csv("/home/omarci/masters/MScDissertation/InfoShield/selected_descriptions_full_LSH_labels.csv")
# 214 + 1 clusters
# 3466 not assigned to cluster

# 3 -> translated text, selected job adverts
infoshield3full = pd.read_csv("/home/omarci/masters/MScDissertation/InfoShield/translated_descriptions_full_LSH_labels.csv")
# 147 + 1 clusters
# 3716 not assigned to cluster

for df in [infoshield1full, infoshield2full, infoshield3full]:
    df.drop(columns=["Unnamed: 0.1", "Unnamed: 0"], inplace=True)