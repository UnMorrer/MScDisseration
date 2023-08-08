# File to combine labels and data, save in a publishable manner/format

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

a = 1