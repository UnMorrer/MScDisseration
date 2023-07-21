# How can I identify significant variables in clustering?
# Variables that "define" clusters -> low intra-cluster variance and high inter-cluster variance
# adjusted rand index???

# Other than InfoShield, do I have other clustering methods available?
import pandas as pd

translatedDf = pd.read_csv("/home/omarci/masters/MScDissertation/data/merged_translated_full.csv")

# InfoShield - 3 interesting clustering methods
# 1 -> unescaped text, all job adverts
infoshield1full = pd.read_csv("/home/omarci/masters/MScDissertation/InfoShield/all_descriptions_full_LSH_labels.csv")
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

# TODO: Only label observations that belong in clusters!

a = 1

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


# Drop duplicate unescaped advert text - experiment
# df = infoshield3full.copy(deep=True)
# df.drop_duplicates(subset=["unescapedJobDesc"])
# All observations preserved - GOOD