import pandas as pd

# InfoShield - 3 interesting clustering methods
# 1 -> unescaped text, all job adverts
infoshield1full = pd.read_csv("/home/omarci/masters/MScDissertation/InfoShield/infoshield1_full_LSH_labels.csv")
print(15 * "-" + "Method 1" + 15 * "-")
print(f"Number of clusters: {len(infoshield1full['LSH label'].unique())}")# 616 + 1 clusters
print(f"Observations not in a cluster: {sum(infoshield1full['LSH label'] == -1)}/{infoshield1full.shape[0]}") # 2468/5022 not assigned to cluster

# 2 -> translated text, all job adverts
infoshield2full = pd.read_csv("/home/omarci/masters/MScDissertation/InfoShield/infoshield2_full_LSH_labels.csv")
print(15 * "-" + "Method 2" + 15 * "-")
print(f"Number of clusters: {len(infoshield2full['LSH label'].unique())}") # 606 + 1 clusters
print(f"Observations not in a cluster: {sum(infoshield2full['LSH label'] == -1)}/{infoshield2full.shape[0]}") # 2703/4214 not assigned to cluster

# 3 -> unescaped text, foreign job adverts
infoshield3full = pd.read_csv("/home/omarci/masters/MScDissertation/InfoShield/infoshield3_full_LSH_labels.csv")
print(15 * "-" + "Method 3" + 15 * "-")
print(f"Number of clusters: {len(infoshield3full['LSH label'].unique())}") # 322 + 1 clusters
print(f"Observations not in a cluster: {sum(infoshield3full['LSH label'] == -1)}/{infoshield3full.shape[0]}") # 1745/4214 not assigned to cluster

# 3 -> unescaped text, foreign job adverts
infoshield4full = pd.read_csv("/home/omarci/masters/MScDissertation/InfoShield/infoshield4_full_LSH_labels.csv")
print(15 * "-" + "Method 3" + 15 * "-")
print(f"Number of clusters: {len(infoshield4full['LSH label'].unique())}") # 313 + 1 clusters
print(f"Observations not in a cluster: {sum(infoshield4full['LSH label'] == -1)}/{infoshield4full.shape[0]}") # 1846/4214 not assigned to cluster

for df in [infoshield1full, infoshield2full, infoshield3full, infoshield4full]:
    df.drop(columns=["Unnamed: 0"], inplace=True)

a = 1