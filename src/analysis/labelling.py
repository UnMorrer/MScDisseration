# How can I identify significant variables in clustering?
# Variables that "define" clusters -> low intra-cluster variance and high inter-cluster variance
# adjusted rand index???
# TODO: Change female and male to gender neutral (reflects reality more...)

# NOTE: Summary of job descriptions that didn't make it to labels.xlsx...
# 5556 total -> 239 above 5k, 257 below 200 characters -> 5060 translated jobs, all there. Woohoo!

# Other than InfoShield, do I have other clustering methods available?
import pandas as pd

translatedDf = pd.read_csv("/home/omarci/masters/MScDissertation/data/merged_translated_full.csv")
descDf = pd.read_csv("/home/omarci/masters/MScDissertation/data/all_descriptions_translated_full.csv")

# InfoShield - 3 interesting clustering methods
# 1 -> unescaped text, all job adverts
infoshield1full = pd.read_csv("/home/omarci/masters/MScDissertation/InfoShield/all_descriptions_translated_full_full_LSH_labels.csv")
# 287 + 1 clusters
# 4424 not assigned to cluster

# 2 -> unescaped text, selected job adverts
infoshield2full = pd.read_csv("/home/omarci/masters/MScDissertation/InfoShield/selected_descriptions_full_LSH_labels.csv")
# 214 + 1 clusters
# 3466 not assigned to cluster

# 3 -> translated text, selected job adverts
infoshield3full = pd.read_csv("/home/omarci/masters/MScDissertation/InfoShield/translated_descriptions_full_LSH_labels.csv")
# 147 + 1 clusters
# 3716 not assigned to cluster

for df in [infoshield1full, infoshield2full, infoshield3full]:
    df.drop(columns=["Unnamed: 0.1", "Unnamed: 0"], inplace=True)

# ? not known
# x good to have
# y MUST HAVE

# Spotting the signs - coding booklet
# Date -> date
# Advertisemet language -> descLanguage
# x Destination country -? locationName
# ? Industry (sector)
# ? Nature of job
# x Contract type
# y Working hours -? isDteJob (4k False, 214 True)
# y Are working hours given in a range?
# y Hourly wage (local currency) -> combination of jobBaseSalaryCurrency + jobBaseSalaryValue(Min/Max)Value + jobBaseSalaryTimeUnit
# y Weekly wage (local currency) -> BUT only ~10% given
# y Monthly wage (local currency)
# x Are wages given in a range?
# y Tax status (reasoning for required: wage comparisons + min wage violation)
# Company name -> jobHiringOrganizationName (companyName has 849 N/A, 857 hiring Organization =/= company name)
# ? Company email -? companyLink (~90% NA)
# x Gender requirements
# x Age requirement
# y Local language requirements
# y Transport to work provided
# y Accommodation provided
# x Accommodation paid or unpaid
# y Indication of shared accommodation
# y Deductions from wages
# y Transfer (or support with it) to destination country provided
# y Previous work experience/skill/qualifications requirements
# x Urgency/immediate departure (start in less than 2 weeks)
# ? Overtime/work on weekends and holidays offered
# y Help settling in provided (e.g. with opening bank accounts or acquiring national insurance number)
# ? Social benefits provided

# n.b. When there are different jobs or positions advertised in one advertisement, record them as separate advertisements giving their identifying number an additional a letter (e.g. a, b)

# For manual inspection of jobs
# pd.set_option('display.max_colwidth', None)
# descDf[descDf.id == 1538].unescapedJobDesc
# Last ID of mine: 3546

# Random select 100 IDs for labelling
# random.sample(idList, sampleSize)
# selectedIds = [866, 891, 907, 943, 954, 1056, 1077, 1120, 1179, 1203, 1239, 1302, 1382, 1437, 1484, 1579, 1675, 1693, 1766, 1835, 1867, 1904, 1935, 1998, 2077, 2078, 2135, 2198, 2266, 2365, 2397, 2469, 2499, 2520, 2631, 2688, 2730, 2743, 2757, 2759, 2762, 2846, 2863, 2962, 3056, 3192, 3304, 3321, 3331, 3354, 3429, 3457, 3473, 3507, 3517, 3529, 3547, 3571, 3637, 3666, 3682, 3710, 3760, 3763, 3822, 3841, 3909, 3917, 3922, 3984, 4214, 4311, 4345, 4506, 4616, 4627, 4649, 4794, 4976, 5005, 5095, 5109, 5152, 5213, 5228, 5231, 5267, 5338, 5586, 5622, 5673, 5680, 5808, 5907, 5936, 5961, 5986, 6102, 6147, 6258]
# selectedTable = descDf[descDf.id.isin(selectedIds)]
# selectedTable[["id", "unescapedJobDesc", "translatedJobDesc"]].to_csv("/home/omarci/masters/MScDissertation/data/selected_labels.csv")

# Investigation of job adverts that "did not make it" to manual labnelling stage
allLabels = "/home/omarci/masters/MScDissertation/data/labels.xlsx"
allJobs = "/home/omarci/masters/MScDissertation/data/all_descriptions.csv"
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
allJobs = pd.read_csv(allJobs)

# Strip letters from ID column in labvelled data
allLabels["cleanID"] = allLabels.id.map(lambda x: x.rstrip("a b c d e f g h i j k l m n o p q r s t u v w x y z"))
allJobs["cleanID"] = allJobs.id.astype(str)

# 529 missing
missingJobs = set(allJobs.cleanID) - set(allLabels.cleanID)

# Character count exclusion + look into how these are unescaped

a = 1