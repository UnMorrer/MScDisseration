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
    "languageProb": float,
    "indTransportToWork": bool,
    "indAccommodationProvided": bool,
    "indSharedAccommodation": bool,
    "indTransferAbroad": bool,
    "indHelpAdministration": bool,
    "totalIndicators": int,
}
# Columns where no data types can be specified
extraCols = ["date", "indWorkingHours", "indWage", "indLocalLanguage", "indWageDeduction", "indNoExperience"]

data = pd.read_csv(data, usecols=(list(dataTypes.keys()) + extraCols), dtype=dataTypes, parse_dates=["date"])

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
    plt.xlim(0, 3000)
    plt.title(plotTitles[colname])

    # Prevent x label cut-off
    plt.tight_layout()

    plt.savefig(f"/home/omarci/masters/MScDissertation/figures/summary_stats/{colname}.png")

categoricalIndicators = [
    "industrySector",
    "jobNature",
    "contractType",
    # "workHoursInRange",
    # "wagesInRange",
    # "taxStatus",
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
    # "socialBenefits"
]

# Indicators - separate df as Hungary and not specified need to be dropped from label data
# Indicators - variables with MANY more possible labels than others
# industrySector
# Age Requirements? -> not show as only a couple exist
foreignData = data[~data["destCountry"].isin(["hungary", "not specified"])].copy() # 2862 rows

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
    "accommodationPaidByWorker": "Accommodation paid by",
    "sharedAccommodation": "Accommodation in shared rooms",
    "deductionFromWages": "Deduction from wage/salary",
    "transferAbroadProvided": "Help with transfer/relocation abroad provided",
    "previousExperience": "Previous experience/training required",
    "urgentDeparture": "Urgent start date (<2 weeks)",
    "overtimeOffered": "Overtime offered",
    "helpSettingIn": "Help with administration (in destination country) provided",
    "socialBenefits": "Employee eligible for social security (in destination country)"
}

# Replace Free -> Employer in accommodation paid by column
foreignData.replace(to_replace="free", value="employer", inplace=True)
# Add in line break for labels
foreignData.replace(to_replace="knowing foreign language is an advantage", value="knowing foreign language\n is an advantage", inplace=True)
foreignData.replace(to_replace="previous work experience is an advantage", value="previous work experience\n is an advantage", inplace=True)

for colname in categoricalIndicators:
    value_counts = foreignData[colname].fillna(value="Not specified").value_counts()
    if colname == "industrySector": # Trim values in big graph
        value_counts = value_counts[value_counts >= 10]

    # Clear plot area
    plt.clf()
    # Create barplot
    plot = sns.barplot(y=value_counts.index.str.title(), x=value_counts.values, color="white", edgecolor="black", linewidth=0.5)
    # Create distinct bar pattern
    for i, bar in enumerate(plot.patches):
        bar.set_hatch(**next(styles))
    # Add thin horizontal grid lines
    plt.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='gray')
    # Rotate x axis text
    plt.xlim(0, 3000)
    plt.xlabel("Number of adverts")
    plt.title(catPlots[colname])

    # Prevent x label cut-off
    plt.tight_layout()

    plt.savefig(f"/home/omarci/masters/MScDissertation/figures/summary_stats/{colname}.png")

############################
# Numeric data
############################

# Working hours (per week)
plt.clf()
sns.boxplot(
    x=foreignData["workHoursPerWeek"],
    y=foreignData["jobNature"].fillna("not specified").str.capitalize(),
    color="gray")
plt.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='gray')
plt.xlabel("Working hours (per week)")
plt.ylabel("Job nature")
plt.title("Working hours by job nature")
plt.tight_layout()
plt.savefig(f"/home/omarci/masters/MScDissertation/figures/summary_stats/workHoursPerWeek.png")

############################
# Indicator data
############################
# Explain what is derived from where
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

# Indicator prevalence - Each indicator present in % of job ads
indicatorPresent = []
labels = []

for col in indicatorCols.keys():
    number = sum(foreignData[col] == True)
    indicatorPresent.append(number)
    labels.append(indicatorCols[col])

# Clear plot area
plt.clf()
# Create barplot
plot = sns.barplot(y=labels, x=indicatorPresent, color="white", edgecolor="black", linewidth=2)
# Create distinct bar pattern
for i, bar in enumerate(plot.patches):
    bar.set_hatch(**next(styles))
# Add thin horizontal grid lines
plt.grid(which='major', axis='x', linestyle='--', linewidth=0.5, color='gray')
plt.xlabel("Number of adverts")
plt.xlim(0, 1000)
plt.title("Number of jobs containing each indicator")
# Prevent x label cut-off
plt.tight_layout()
plt.savefig(f"/home/omarci/masters/MScDissertation/figures/summary_stats/indicatorPrevalence.png")



# Number of indicators in job ads - histogram
value_counts = foreignData["totalIndicators"].value_counts().sort_index()

# Clear plot area
plt.clf()
# Create barplot
plot = sns.barplot(x=value_counts.index, y=value_counts.values, color="white", edgecolor="black", linewidth=2)
# Create distinct bar pattern
for i, bar in enumerate(plot.patches):
    bar.set_hatch(**next(styles))
# Add thin horizontal grid lines
plt.grid(which='major', axis='y', linestyle='--', linewidth=0.5, color='gray')
plt.ylabel("Number of adverts")
plt.xlabel("Number of indicators")
plt.title("Number of jobs by indicators present")

# Prevent x label cut-off
plt.tight_layout()
plt.savefig(f"/home/omarci/masters/MScDissertation/figures/summary_stats/totalIndicators.png")


# How are each built up? 1 - indicator, 2 indicators etc.
# Category/Bar: Indicator
# Colour: Number of indicators in the advert
# Bar height: Number of adverts
value_counts = {}

for indicator in indicatorCols.keys():
    value_counts[indicatorCols[indicator]] = foreignData.groupby("totalIndicators")[indicator].apply(lambda x: sum(x.values == True))

value_counts = pd.DataFrame(value_counts).iloc[1: , :]
# Convert into percentage of adverts
value_counts = value_counts.div(value_counts.sum(axis=1), axis=0)*100

plt.clf()
value_counts.plot(kind="bar")

plt.xlabel("Total indicators in advertisement")
plt.ylabel("Percentage of adverts")
plt.title("Breakdown by total indicators in advert")

plt.xticks(rotation=0)
plt.xlim((0.5, 4.5))
plt.ylim((0, 50))
plt.grid(which='major', axis='y', linestyle='--', linewidth=0.5, color='gray')
plt.legend(bbox_to_anchor=(1, 0.40), loc="lower left")
plt.savefig(f"/home/omarci/masters/MScDissertation/figures/summary_stats/indicatorBreakdown.png", bbox_inches="tight")
