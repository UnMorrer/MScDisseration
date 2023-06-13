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
# Exploratory data analysis for jobs without description

df = pd.read_csv("/home/omarci/masters/MScDisseration/data/merged_noDesc.csv")

print(df.shape)

# URL analysis
shortUrl = df['url'].str.slice(0, 25)
print(shortUrl.value_counts())
# 1771 - desc, likely matchable
# 694 - away -> discard
# 45 - jdp -> ?

# Content column - abbreviated job description?
# NO HTML tags tho
print(sum(df.content.isna()))
df["contentLength"] = df["content"].str.len()
# Min 40 - Max 290 characters with 270 average


a = 1