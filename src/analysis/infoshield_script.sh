#!/usr/bin/env bash
# Bash script to run InfoShield for dissertation project

# Make folder to store results in
cd "/home/omarci/masters/MScDissertation/"
rm -rf "InfoShield"; mkdir "InfoShield"

# 1 -> unescaped text, all job adverts
"/home/omarci/.cache/pypoetry/virtualenvs/infoshield--uNm2Cza-py3.10/bin/python" "/home/omarci/masters/InfoShield/infoshield.py" "/home/omarci/masters/MScDissertation/data/final_dataset.csv" "id" "unescapedJobDesc"
# Move results from InfoShield
mv -f "/home/omarci/masters/MScDissertation/results/" "/home/omarci/masters/MScDissertation/InfoShield/allAdverts"
# Move data (LSH) from data folder
mv -f "/home/omarci/masters/MScDissertation/data/final_dataset_full_LSH_labels.csv" "/home/omarci/masters/MScDissertation/InfoShield/infoshield1_full_LSH_labels.csv"
mv -f "/home/omarci/masters/MScDissertation/data/final_dataset_LSH_labels.csv" "/home/omarci/masters/MScDissertation/InfoShield/infoshield1_LSH_labels.csv"
mv -f "/home/omarci/masters/MScDissertation/compression_rate.csv" "/home/omarci/masters/MScDissertation/InfoShield/allAdverts/compression_rate.csv"
mv -f "/home/omarci/masters/MScDissertation/template_table.csv" "/home/omarci/masters/MScDissertation/InfoShield/allAdverts/template_table.csv"

# 2 -> translated text, all job adverts
"/home/omarci/.cache/pypoetry/virtualenvs/infoshield--uNm2Cza-py3.10/bin/python" "/home/omarci/masters/InfoShield/infoshield.py" "/home/omarci/masters/MScDissertation/data/final_dataset.csv" "id" "translatedJobDesc"
# Move results from InfoShield
mv -f "/home/omarci/masters/MScDissertation/results/" "/home/omarci/masters/MScDissertation/InfoShield/selectedAdverts"
# Move data (LSH) from data folder
mv -f "/home/omarci/masters/MScDissertation/data/final_dataset_full_LSH_labels.csv" "/home/omarci/masters/MScDissertation/InfoShield/infoshield2_full_LSH_labels.csv"
mv -f "/home/omarci/masters/MScDissertation/data/final_dataset_LSH_labels.csv" "/home/omarci/masters/MScDissertation/InfoShield/infoshield2_LSH_labels.csv"
mv -f "/home/omarci/masters/MScDissertation/compression_rate.csv" "/home/omarci/masters/MScDissertation/InfoShield/selectedAdverts/compression_rate.csv"
mv -f "/home/omarci/masters/MScDissertation/template_table.csv" "/home/omarci/masters/MScDissertation/InfoShield/selectedAdverts/template_table.csv"

# 3 -> unescaped text, abroad job adverts
"/home/omarci/.cache/pypoetry/virtualenvs/infoshield--uNm2Cza-py3.10/bin/python" "/home/omarci/masters/InfoShield/infoshield.py" "/home/omarci/masters/MScDissertation/data/abroad_only_final.csv" "id" "unescapedJobDesc"
# Move results from InfoShield
mv -f "/home/omarci/masters/MScDissertation/results/" "/home/omarci/masters/MScDissertation/InfoShield/selectedAdverts"
# Move data (LSH) from data folder
mv -f "/home/omarci/masters/MScDissertation/data/abroad_only_final_full_LSH_labels.csv" "/home/omarci/masters/MScDissertation/InfoShield/infoshield3_full_LSH_labels.csv"
mv -f "/home/omarci/masters/MScDissertation/data/abroad_only_final_LSH_labels.csv" "/home/omarci/masters/MScDissertation/InfoShield/infoshield3_LSH_labels.csv"
mv -f "/home/omarci/masters/MScDissertation/compression_rate.csv" "/home/omarci/masters/MScDissertation/InfoShield/selectedAdverts/compression_rate.csv"
mv -f "/home/omarci/masters/MScDissertation/template_table.csv" "/home/omarci/masters/MScDissertation/InfoShield/selectedAdverts/template_table.csv"

# 4 -> translated text, abroad job adverts
"/home/omarci/.cache/pypoetry/virtualenvs/infoshield--uNm2Cza-py3.10/bin/python" "/home/omarci/masters/InfoShield/infoshield.py" "/home/omarci/masters/MScDissertation/data/abroad_only_final.csv" "id" "translatedJobDesc"
# Move results from InfoShield
mv -f "/home/omarci/masters/MScDissertation/results/" "/home/omarci/masters/MScDissertation/InfoShield/translatedAdverts"
# Move data (LSH) from data folder
mv -f "/home/omarci/masters/MScDissertation/data/abroad_only_final_full_LSH_labels.csv" "/home/omarci/masters/MScDissertation/InfoShield/infoshield4_full_LSH_labels.csv"
mv -f "/home/omarci/masters/MScDissertation/data/abroad_only_final_LSH_labels.csv" "/home/omarci/masters/MScDissertation/InfoShield/infoshield4_LSH_labels.csv"
mv -f "/home/omarci/masters/MScDissertation/compression_rate.csv" "/home/omarci/masters/MScDissertation/InfoShield/translatedAdverts/compression_rate.csv"
mv -f "/home/omarci/masters/MScDissertation/template_table.csv" "/home/omarci/masters/MScDissertation/InfoShield/translatedAdverts/template_table.csv"