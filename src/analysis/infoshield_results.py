import pandas as pd

# InfoShield - 3 interesting clustering methods
# 1 -> unescaped text, all job adverts
infoshield1full = pd.read_csv("/home/omarci/masters/MScDissertation/InfoShield/all_descriptions_translated_full_LSH_labels.csv")
print(15 * "-" + "Method 1" + 15 * "-")
print(f"Number of clusters: {len(infoshield1full['LSH label'].unique())}")# 616 + 1 clusters
print(f"Observations not in a cluster: {sum(infoshield1full['LSH label'] == -1)}/{infoshield1full.shape[0]}") # 2485/5058 not assigned to cluster

# 2 -> unescaped text, selected job adverts
infoshield2full = pd.read_csv("/home/omarci/masters/MScDissertation/InfoShield/selected_descriptions_full_LSH_labels.csv")
print(15 * "-" + "Method 2" + 15 * "-")
print(f"Number of clusters: {len(infoshield2full['LSH label'].unique())}") # 425 + 1 clusters
print(f"Observations not in a cluster: {sum(infoshield2full['LSH label'] == -1)}/{infoshield2full.shape[0]}") # 2358/4214 not assigned to cluster

# 3 -> translated text, selected job adverts
infoshield3full = pd.read_csv("/home/omarci/masters/MScDissertation/InfoShield/translated_descriptions_full_LSH_labels.csv")
print(15 * "-" + "Method 3" + 15 * "-")
print(f"Number of clusters: {len(infoshield3full['LSH label'].unique())}") # 386 + 1 clusters
print(f"Observations not in a cluster: {sum(infoshield3full['LSH label'] == -1)}/{infoshield3full.shape[0]}") # 2586/4214 not assigned to cluster

for df in [infoshield1full, infoshield2full, infoshield3full]:
    df.drop(columns=["Unnamed: 0.1", "Unnamed: 0"], inplace=True)

a = 1