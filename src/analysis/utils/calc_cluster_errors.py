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