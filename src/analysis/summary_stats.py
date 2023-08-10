import pandas as pd
import matplotlib.pyplot as plt # This import takes ages
import seaborn as sns
import numpy as np
from cycler import cycler

hatch_cycle = (cycler('hatch', ['///', '||', '--', '...','\///', 'xxx', '\\\\']))
styles = hatch_cycle()
data = "/home/omarci/masters/MScDissertation/data/final_dataset.csv"
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
    "socialBenefits": str,
    "jobTitle": str,
    "jobHiringOrganizationName": str,
    "unescapedJobDesc": str,
    "translatedJobDesc": str,
    "descLanguage": str,
    "languageProb": float
}

data = pd.read_csv(data, usecols=(list(dataTypes.keys()) + ["date"]), dtype=dataTypes, parse_dates=["date"])

# Interesting summary statistics:
# Destination country
# Language
# Drop Hungary + Not Specified? -> Most likely yes
# Prevalence of indicators

plotTitles = {
    "destCountry": "Country of destination",
    "descLanguage": "Job description language"
}

for colname in ["destCountry", "descLanguage"]:
    value_counts = data[colname].value_counts()
    # Limit to at least 10 ads to reduce clutter. TODO: Mention in text or in appendix
    value_counts = value_counts[value_counts >= 10]

    # Replace values with more readable ones for language
    if colname == "descLanguage":
        value_counts.rename(index={
            "hu": "Hungarian",
            "en": "English",
            "de": "German",
            "lt": "Lithuanian",
            "pl": "Polish",
            "ru": "Russian",
            "uk": "Ukrainian"
        }, inplace=True)

    # Clear plot area
    plt.clf()
    # Create barplot
    plot = sns.barplot(y=value_counts.index.str.title(), x=value_counts.values, color="white", edgecolor="black", linewidth=2)
    # Create distinct bar pattern
    for i, bar in enumerate(plot.patches):
        bar.set_hatch(**next(styles))
    # Add thin horizontal grid lines
    plt.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='gray')
    plt.xlabel("Number of adverts")
    plt.title(plotTitles[colname])

    # Prevent x label cut-off
    plt.tight_layout()

    plt.savefig(f"/home/omarci/masters/MScDissertation/figures/summary_stats/{colname}.png")

categoricalIndicators = [
    # "industrySector",
    "jobNature",
    "contractType",
    "workHoursInRange",
    "wagesInRange",
    "taxStatus",
    "genderRequirements",
    # "ageRequirements",
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
    "socialBenefits"
]

# Indicators - separate df as Hungary and not specified need to be dropped from label data
# Indicators - variables with MANY more possible labels than others
# industrySector
# Age Requirements? -> not show as only a couple exist
foreignData = data[~data["destCountry"].isin(["hungary", "not specified"])] # 2862 rows

# TODO: How to fill/amend data with "Not Specified"?

catPlots = {
    "industrySector": "Job industry/sector",
    "jobNature": "Job nature",
    "contractType": "Job contract duration",
    "workHoursInRange": "Working hours in range",
    "wagesInRange": "Wage/Salary in range",
    "taxStatus": "Wage/Salary tax status",
    "genderRequirements": "Gender requirement",
    "ageRequirements": "Age requirement",
    "localLanguageRequirements": "Local language proficiency required",
    "transportToWorkProvided": "Transport to workplace organized",
    "accommodationProvided": "Accommodation provided",
    "accommodationPaidByWorker": "Accommodation paid by", #NOTE: Change Free -> Employer
    "sharedAccommodation": "Accommodation in shared rooms",
    "deductionFromWages": "Deduction from wage/salary",
    "transferAbroadProvided": "Help with transfer/relocation abroad provided",
    "previousExperience": "Previous experience/training required",
    "urgentDeparture": "Urgent start date (<2 weeks)",
    "overtimeOffered": "Overtime offered",
    "helpSettingIn": "Help with administration (in destination country) provided",
    "socialBenefits": "Employee eligible for social security (in destination country)"
}

for colname in categoricalIndicators:
    value_counts = foreignData[colname].value_counts()
    value_counts = value_counts[value_counts >= 10]

    # Clear plot area
    plt.clf()
    # Create barplot
    plot = sns.barplot(x=value_counts.index.str.title(), y=value_counts.values, color="white", edgecolor="black", linewidth=2)
    # Create distinct bar pattern
    for i, bar in enumerate(plot.patches):
        bar.set_hatch(**next(styles))
    # Add thin horizontal grid lines
    plt.grid(which='major', axis='y', linestyle='--', linewidth=0.5, color='gray')
    # Rotate x axis text
    plt.xticks(rotation=90)
    plt.ylabel("Number of adverts")
    plt.title(catPlots[colname])

    # Prevent x label cut-off
    plt.tight_layout()

    plt.savefig(f"/home/omarci/masters/MScDissertation/figures/summary_stats/{colname}.png")

a = 1