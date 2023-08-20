# Compare 100 labels Me vs Ema#
# My last ID 3546 - Compare stuff I labelled twice and look for within-myself variance
# TODO: Cockbain paper - Cohen’s Kappa for nominal variables and Krippendorff Alpha for ratio variables: Evaluation between people!

import pandas as pd
import numpy as np

allLabels = "/home/omarci/masters/MScDissertation/data/labels.xlsx"
emaLabels = "/home/omarci/masters/MScDissertation/data/selected_labels_Ema.xlsx"
marcellLabels = "/home/omarci/masters/MScDissertation/data/selected_labels_Marcell.xlsx"
IDs = [866, 891, 907, 943, 954, 1056, 1077, 1120, 1179, 1203, 1239, 1302, 1382, 1437, 1484, 1579, 1675, 1693, 1766, 1835, 1867, 1904, 1935, 1998, 2077, 2078, 2135, 2198, 2266, 2365, 2397, 2469, 2499, 2520, 2631, 2688, 2730, 2743, 2757, 2759, 2762, 2846, 2863, 2962, 3056, 3192, 3304, 3321, 3331, 3354, 3429, 3457, 3473, 3507, 3517, 3529, 3547, 3571, 3637, 3666, 3682, 3710, 3760, 3763, 3822, 3841, 3909, 3917, 3922, 3984, 4214, 4311, 4345, 4506, 4616, 4627, 4649, 4794, 4976, 5005, 5095, 5109, 5152, 5213, 5228, 5231, 5267, 5338, 5586, 5622, 5673, 5680, 5808, 5907, 5936, 5961, 5986, 6102, 6147, 6258]
selectedIDs = [str(ID) for ID in IDs]
marcellIDs = [str(ID) for ID in IDs if ID <= 3546]
emaIDs = [str(ID) for ID in IDs if ID > 3546 and ID != 4794]
dataTypes = {
    "id": str,
    "destCountry": str,
    "industrySector": str,
    "jobNature": str,
    "contractType": str,
    "workHoursPerWeek": float,
    "workHoursInRange": str,
    "hourlyWage": float,
    "weeklyWage": float,
    "monthlyWage": float,
    "wagesInRange": str,
    "taxStatus": str,
    "genderRequirements": str,
    "ageRequirements": str,
    "localLanguageRequirements": str,
    "transportToWorkProvided": str,
    "accommodationProvided": str,
    "accommodationPaidByWorker": str,
    "sharedAccommodation": str,
    "deductionFromWages": str,
    "transferAbroadProvided": str,
    "previousExperience": str,
    "urgentDeparture": str,
    "overtimeOffered": str,
    "helpSettingIn": str,
    "socialBenefits": str
}

allLabels = pd.read_excel(allLabels, usecols=list(dataTypes.keys()), na_values=["Not specified", "not specified"]).astype(dataTypes)
emaLabels = pd.read_excel(marcellLabels, na_values="Not specified").astype(dataTypes)
marcellLabels = pd.read_excel(marcellLabels, na_values="Not specified").astype(dataTypes)

# Labeler alignment comparison
print(f"Labeler alignment: {emaLabels.compare(marcellLabels)}")

# Prepare for comparison with all labels
emaLabels.drop(columns=["unescapedJobDesc", "translatedJobDesc"], inplace=True)
marcellLabels.drop(columns=["unescapedJobDesc", "translatedJobDesc"], inplace=True)
emaLabels = emaLabels[emaLabels.id.isin(emaIDs)].copy().sort_values("id").reset_index(drop=True)
marcellLabels = marcellLabels[marcellLabels.id.isin(marcellIDs)].copy().sort_values("id").reset_index(drop=True)

allLabelsEma = allLabels[allLabels.id.isin(emaIDs)].sort_values("id").reset_index(drop=True)
allLabelsMarcell = allLabels[allLabels.id.isin(marcellIDs)].sort_values("id").reset_index(drop=True)

emaCompared = allLabelsEma.compare(emaLabels)
marcellCompared = allLabelsMarcell.compare(marcellLabels)

print(f"Comparison between Ema and future labels: {emaCompared}")
print(f"Comparison between Marcell and future labels: {marcellCompared}")
# Number of misaligned labels + distribution
# NOTE: NaN-related mislabeling is NOT counted in below!
print(f"Ema-label, mislabeling by column name: {allLabelsEma.ne(emaLabels).sum(axis=0)}")
print(f"Marcell-label, mislabeling by column name: {allLabelsMarcell.ne(marcellLabels).sum(axis=0)}")

# Add ID to saved result for further analysis
emaCompared = emaCompared.merge(marcellLabels.id, left_index=True, right_index=True)
marcellCompared = marcellCompared.merge(marcellLabels.id, left_index=True, right_index=True)

# Within-labeler variance - save for further analysis
# Most due to industry/sector available in labels, job nature, working hours range, and previous experience
emaCompared.to_csv("/home/omarci/masters/MScDissertation/data/ema_compare_labels.csv")

# Most due to much better job nature categorization in all/finished labels AND working hours
marcellCompared.to_csv("/home/omarci/masters/MScDissertation/data/marcell_compare_labels.csv")
# TODO: Increased quality of data - mention in the dissertation + important for showing contribution
