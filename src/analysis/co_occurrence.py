# Script to calculate co-occurrence matrix of indicators
import pandas as pd
import numpy as np

data = "/home/omarci/masters/MScDissertation/data/final_dataset.csv"
dataTypes = {
    "id": int,
    "destCountry": str,
    "unescapedJobDesc": str,
    "translatedJobDesc": str,
    "descLanguage": str,
    "indTransportToWork": bool,
    "indAccommodationProvided": bool,
    "indSharedAccommodation": bool,
    "indTransferAbroad": bool,
    "indHelpAdministration": bool,
    "totalIndicators": int,
    # Additional stuff - might not be needed AT ALL
    "industrySector": str,
    "jobNature": str,
    "contractType": str,
    "genderRequirements": str,
    "ageRequirements": str,
    "accommodationPaidByWorker": str,
    "urgentDeparture": str,
    "overtimeOffered": str,
    "socialBenefits": str,
}
indicatorCols = {
    "indWorkingHours": "Working hours above legal limit",
    "indWage" : "Wage below national minimum",
    "indLocalLanguage" : "Local language not required",
    "indTransportToWork" : "Transport to work provided",
    "indAccommodationProvided" : "Accommodation provided",
    "indSharedAccommodation" : "Shared accommodation",
    "indWageDeduction" : "Deduction from wages",
    "indTransferAbroad" : "Transfer abroad provided",
    "indNoExperience" : "No prior experience required",
    "indHelpAdministration" : "Help with administration"
}

pandasData = pd.read_csv(data, usecols=indicatorCols.keys(), dtype=dataTypes).fillna(0).astype(int)
data = pandasData.to_numpy() # So that I can track labels

coOccurrenceMatrix = np.dot(data.transpose(), data)
coOccurrenceMatrixDiag = np.diagonal(coOccurrenceMatrix)
with np.errstate(divide='ignore', invalid='ignore'):
    coOccurrenceMatrixPercent = np.nan_to_num(np.true_divide(coOccurrenceMatrix, coOccurrenceMatrixDiag[:, None]))

# Remove values above diagonal
coOccurrenceMatrix = np.tril(coOccurrenceMatrix, k=0)

pandasMatrix = pd.DataFrame(data=coOccurrenceMatrix, columns=indicatorCols.values(), index=indicatorCols.values()).replace(to_replace=0, value="")

print(pandasMatrix.to_latex(index=True))

a = 1