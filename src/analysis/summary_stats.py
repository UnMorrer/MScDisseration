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
foreignData = data[~data["destCountry"].isin(["hungary", "not specified"])] # 2862 rows

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
    value_counts = foreignData[colname].fillna(value="Not specified").value_counts()
    value_counts = value_counts[value_counts >= 10]

    # Clear plot area
    plt.clf()
    # Create barplot
    plot = sns.barplot(y=value_counts.index.str.title(), x=value_counts.values, color="white", edgecolor="black", linewidth=2)
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

# Monthly net wage


# Number of indicators present
# Countries/observations with wages:
wageData = foreignData[~foreignData.monthlyWage.isna() | ~foreignData.weeklyWage.isna() | ~foreignData.hourlyWage.isna()]
print(f"Number of rows with wage data: {wageData.shape[0]}")
print(f"Countries with wage data: {wageData.destCountry.unique().tolist()}")
# DE, AT, PL, NL, BE, LT, FI, SE

workHoursData = foreignData[~foreignData.workHoursPerWeek.isna()]
print(f"Number of rows with work hours data: {wageData.shape[0]}")
print(f"Countries with work hours data: {wageData.destCountry.unique().tolist()}")

minWagePerCountry = {
    # Minimum wage in each country (gross EUR)
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
        "spain": 290.77,
    },
}

def indicate_low_wage(row):
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
    # destCountry
    # workingHours
    # jobNature - to impute above
    # contractType
    pass


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
def indicate_long_hours(row):
    """
    Function to check if the weekly
    working hours exceed the national maximum

    Inputs:
    row - pd.Series: Pandas Series containing
    a full row's worth of data

    Returns:
    long_hours - bool: Boolean indicator. True
    if working hours exceed national maximum
    """
    # destCountry
    # workingHours
    # contractType
    pass

complexIndicators = {
    "workingHours": lambda row: row, # TODO: Implement - this will need to be country-specific
    "wage": lambda row: row, # TODO: Implement - this will need to be country-specific
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

# Different kind of plot for numeric data: working hours, wages, number of indicators etc.
numericIndicators = [
    "workHoursPerWeek",
    "monthlyNetWage",
    "numberOfIndicators"
]

a = 1