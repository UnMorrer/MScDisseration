# Exploratory Data Analysis for jobs with only description
import pandas as pd

df = pd.read_csv("/home/omarci/masters/MScDisseration/data/merged_onlyDesc.csv")

# Size
print(df.shape)
# No UID rows
print(sum(df.uid.isna()))
# URL composition - all missing
print(sum(df.url.isna()))
# Job description - ALL have
print(sum(df.jobDescription.isna()))
# NO URL or UID - Can I use the job description to match
a = 1