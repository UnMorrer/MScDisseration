# File to combine labels and data, save in a publishable manner/format
# TODO: Move indicator calculation details to appendix or paper (defo Overleaf)

import pandas as pd
import re

labels = "/home/omarci/masters/MScDissertation/data/labels.xlsx"
translations = "/home/omarci/masters/MScDissertation/data/all_descriptions_translated_full.csv"

labelDataTypes = {
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
translationDataTypes = {
    "id": str,
    "jobTitle": str,
    "jobHiringOrganizationName": str,
    "unescapedJobDesc": str,
    "translatedJobDesc": str,
    "descLanguage": str,
    "languageProb": float
}
lowerCaseColumns = [
    "destCountry",
    "industrySector",
    "jobNature",
    "contractType",
    "workHoursInRange",
    "wagesInRange",
    "taxStatus",
    "genderRequirements",
    "ageRequirements",
    "localLanguageRequirements",
    "transportToWorkProvided",
    "accommodationProvided",
    "accommodationPaidByWorker",
    "sharedAccommodation",
    "deductionFromWages",
    "transferAbroadProvided",
    "previousExperience",
    "urgentDeparture",
    "overtimeOffered",
    "helpSettingIn",
    "socialBenefits",
    "jobTitle",
    "jobHiringOrganizationName",
    "descLanguage",
    ]
letters = "a b c d e f g h i j k l m n o p q r s t u v w x y z"

labels = pd.read_excel(labels, usecols=list(labelDataTypes.keys()), na_values=["Not specified", "not specified"], dtype=labelDataTypes)
translations = pd.read_csv(translations, usecols=(list(translationDataTypes.keys()) + ["date"]), dtype=translationDataTypes, parse_dates=["date"])

# Adverts with multiple jobs (labels)
# -> Exclude from analysis
# -> BUT upload as part of the data. Use 1 (advert data) : m (labels) join
labels["cleanId"] = labels.id.map(lambda x: x.rstrip(letters)).astype(str)
translations.rename(columns={"id": "cleanId"}, inplace=True)

joinedLabels = labels.merge(translations, on="cleanId", how="left")

# Lowercase label column values
for colname in lowerCaseColumns:
    joinedLabels[colname] = joinedLabels[colname].str.lower()

# Change female and male to gender neutral (reflects reality more...)
joinedLabels.replace(to_replace="female and male", value="gender neutral", inplace=True)

# Drop identifier data and save publishable data
publishData = joinedLabels.drop(columns=["id", "cleanId"])
publishData.to_csv("/home/omarci/masters/MScDissertation/data/public_dataset.csv", na_rep="NA", encoding='utf-8-sig')

# Drop jobs with multiple adverts - 5023 adverts remain
joinedLabels = joinedLabels[~joinedLabels["id"].str.contains("[a-zA-Z]").fillna(False)]

# Create indicators
# Number of indicators present
# Countries/observations with wages:
wageData = foreignData[~foreignData.monthlyWage.isna() | ~foreignData.weeklyWage.isna() | ~foreignData.hourlyWage.isna()]
print(f"Number of rows with wage data: {wageData.shape[0]}")
print(f"Countries with wage data: {wageData.destCountry.unique().tolist()}")
# DE, AT, PL, NL, BE, LT, FI, SE

workHoursData = foreignData[~foreignData.workHoursPerWeek.isna()]
print(f"Number of rows with work hours data: {wageData.shape[0]}")
print(f"Countries with work hours data: {wageData.destCountry.unique().tolist()}")

# TODO: Move these details to appendix or paper (defo Overleaf)
minWagePerCountry = {
    "tax excluded" : {
        "hourlyWage" : {
            "belgium": 11.28,
            "germany": 12,
            "lithuania": 4.04,
            "netherlands": 9.3,
            "poland": 4.86,
            "spain": 7.27,
        },
        "weeklyWage" : {
            "belgium": 451.15,
            "germany": 480,
            "lithuania": 193.85,
            "netherlands": 446.4,
            "poland": 171.75,
            "spain": 290.77,
        },
        "monthlyWage" : {
            "belgium": 451.15,
            "germany": 480,
            "lithuania": 193.85,
            "netherlands": 446.4,
            "poland": 171.75,
            "spain": 1080,
        },
    },
    "tax included" : {
        "hourlyWage" : {
            "belgium": 7.62,
            "germany": 8.57,
            "lithuania": 3.04,
            "netherlands": 8.53,
            "poland": 3.79,
            "spain": 6.81,
        },
        "weeklyWage" : {
            "belgium": 304.62,
            "germany": 342.92,
            "lithuania": 146.08,
            "netherlands": 409.38,
            "poland": 171.75,
            "spain": 272.33,
        },
        "monthlyWage" : {
            "belgium": 1320,
            "germany": 1486,
            "lithuania": 633,
            "netherlands": 1774,
            "poland": 579.92,
            "spain": 1011.52,
        },
    }
}

maxWorkHoursPerCountry = {
    "short-term" : {
        "austria": 60,
        "belgium": 40,
        "finland": 40,
        "germany": 48,
        "lithuania": 60,
        "netherlands": 60,
        "poland": 48,
        "spain": 40,
        "sweden": 48,
        "switzerland": 50,
    },
    "long-term" : {
        "austria": 48,
        "belgium": 40,
        "finland": 40,
        "germany": 48,
        "lithuania": 48,
        "netherlands": 48,
        "poland": 48,
        "spain": 40,
        "sweden": 48,
        "switzerland": 50,
    },
}


# NOTE: Maybe print ID for double-checking...
def indicate_low_wage(row, countryData = minWagePerCountry):
    """
    Function to check if the hourly wage on
    offered is below the national minimum
    wage. 

    Assumptions:
    If no working hours per week given,

    Inputs:
    row - pd.Series: Pandas Series containing
    a full row's worth of data

    Returns:
    low_wage - bool: Boolean indicator. True
    if wage offered is below national minimum
    """
    # Return NA for countries with no data
    if row.destCountry not in countryData["tax excluded"]["hourlyWage"].keys():
        return np.nan

    # Return N/A for observations with no wage data
    if row.hourlyWage.isna() and row.weeklyWage.isna() and row.monthlyWage.isna():
        return np.nan

    # Use tax status given or gross if N/A (best comparison)
    tax = row.taxStatus
    if tax.isna():
        tax = "tax excluded"

    # Best option: Monthly wage, weekly wage - compare direct
    if not row.monthlyWage.isna():
        wage = row.monthlyWage
        return wage < countryData[tax]["monthlyWage"][row.destCountry]
    if not row.weeklyWage.isna():
        wage = row.weeklyWage
        return wage < countryData[tax]["weeklyWage"][row.destCountry]
    if (not row.hourlyWage.isna()) and (not row.workHoursPerWeek.isna()):
        wage = row.hourlyWage * row.workHoursPerWeek
        return wage < countryData[tax]["weeklyWage"][row.destCountry]

    # If no work hours are given, compare estimates to my calculated values
    return row.hourlyWage < countryData[tax]["hourlyWage"][row.destCountry]


def indicate_long_hours(row, countryData=maxWorkHoursPerCountry):
    """
    Function to check if the weekly
    working hours exceed the national maximum

    Inputs:
    row - pd.Series: Pandas Series containing
    a full row's worth of data
    countryData - dictionary: Dictionary with keys
    long-term and short-term that contain relevant
    working hours regulations for countries

    Returns:
    longHours - bool: Boolean indicator. True
    if working hours exceed national maximum
    """

    # Return N/A if working hours not given
    if row.workHoursPerWeek.isna():
        return np.nan

    # Check we can analyze country
    if row.destCountry not in maxWorkHoursPerCountry["short-term"].keys():
        return np.nan

    # Apply loose criteria if contract duration not specified
    if row.contractType.isna():
        contract = "short-term"
    else:
        contract = row.contractType

    # Look up criteria
    return row.workHoursPerWeek > maxWorkHoursPerCountry[contract][row.destCountry]

complexIndicators = {
    "workingHours": indicate_long_hours,
    "wage": indicate_low_wage,
}

indicators = {
    "localLanguage": lambda x: x.lower() == "none",
    "transportToWork": lambda  x: x.lower() == "yes",
    "accommodationProvided": lambda x: x.lower() == "yes",
    "sharedAccommodation": lambda x: x.lower() != "no" or x.lower() != "not specified",
    "wageDeduction": lambda x: x.lower() == "yes",
    "transferAbroad": lambda x: x.lower() != "no" or x.lower() != "not specified",
    "previousExperience": lambda x: x.lower() == "no",
    "helpSettingIn": lambda x: x.lower() == "yes",
}

joinedLabels.to_csv("/home/omarci/masters/MScDissertation/data/final_dataset.csv", na_rep="NA", encoding='utf-8-sig')

a = 1