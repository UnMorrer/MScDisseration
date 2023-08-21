# Python file that contains cluster mean (squared) error calculation methods
import pandas as pd
import numpy as np

##########################################
# Evaluation functions
##########################################

def within_cluster_dispersion(data, usevars, label="LSH label", power=1):
    """
    Function to calculate within-cluster dispersion
    Formula: https://scikit-learn.org/stable/modules/clustering.html#clustering-pWerformance-evaluation
    2.3.11.6 W_k - Within-cluster dispersion

    Inputs:
    data - pd.DataFrame: Dataframe that contains
    the data for the analysis
    usevars - [str]: List of column names
    in data that are used to calculate dispersion metric
    label - str: Column name in dataframe that contains
    label assignment
    power - int: Controls dispersion metric. Power=2
    calculates variance while power=1 calculates
    (raw) differences.

    Returns:
    dispersion - pd.Series: Series that contains
    the calculated dispersion for each cluster.
    Sum up to obtain values for the entire dataset
    """
    df = data[usevars+[label]].copy()

    # Calculate centroid locations for each cluster
    centroids = df.groupby(label).mean()

    # Apply dispersion calculation for each row/observation
    df["dispersion"] = df.apply(lambda row: np.sum(np.abs(row[usevars] - centroids.loc[row[label]])**power), axis=1)

    return df[[label, "dispersion"]].groupby(label).sum()

def assign_label(value):
    """
    Function to assign clusters into groups by size
    """
    if value == 2:
        return '2'
    elif value == 3:
        return '3'
    elif value == 4:
        return '4'
    elif value >= 5 and value <= 9:
        return '5-9'
    elif value >= 10 and value <= 19:
        return '10-19'
    elif value >= 20:
        return '20+'


def calculate_grouped_results(size, differences, labelName="LSH label", labelOrder=["2", "3", "4", "5-9", "10-19", "20+"]):
    """
    Function to group mean abs error calculated by
    within_cluster_dispersion into clusters by
    cluster size

    Inputs:
    size - pd.DataFrame with columns 'labelName' and
    'clusterSize' which desribes how many observations
    there are within each cluster.
    (-1 cluster can be dropped as it's not part of analysis)
    differences - pd.Dataframe with columns 'labelName' and
    'dispersion' (corresponds to standard output of 
    function above)
    labelOrder - [str]: How to order clustering groups
    returned by assign_label function (above)

    Returns:
    diffGraph - pd.DataFrame with rows as entries and columns
    'avgDiff', 'clusterGroup' and 'clusterSize' that contain
    the data required for graphing
    """
    df = size.copy(deep=True)
    df["clusterGroup"] = df["clusterSize"].apply(assign_label)
    df = df.merge(differences.reset_index().rename(columns={"dispersion":"diff"}), on=labelName, how="inner")
    df["avgDiff"] = df["diff"]/df["clusterSize"]

    weighted_mean = lambda x: np.average(x, weights=df.loc[x.index, "clusterSize"])

    diffGraph = df.groupby("clusterGroup").agg(weightedMean=("avgDiff", weighted_mean))

    # Reorder index
    diffGraph = diffGraph.loc[labelOrder]

    return diffGraph

if __name__ == "__main__":
    # Motivating toy example - max mean error is len(numIndicators)
    data = pd.DataFrame(
        data=[[1, 0, 0, 0, 0], [1, 1, 1, 1, 1], [1, 0, 0, 0, 0], [1, 1, 1, 1, 1]],
        columns=["LSH label", "col1", "col2", "col3", "col4"])
    # n =1 differences
    dispersion = within_cluster_dispersion(data, ["col1", "col2", "col3", "col4"])

    a = 1