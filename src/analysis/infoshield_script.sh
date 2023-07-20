#!/usr/bin/env bash
# Bash script to run InfoShield for dissertation project

# Make folder to store results in
cd "/home/omarci/masters/MScDissertation/"
rm -rf "results/InfoShield"; mkdir "results/InfoShield"

# 1 -> unescaped text, all job adverts
"/home/omarci/.cache/pypoetry/virtualenvs/infoshield--uNm2Cza-py3.10/bin/python" infoshield.py "/home/omarci/masters/MScDisseration/data/all_descriptions.csv" "id" "unescapedJobDesc"
# Move results from InfoShield
mv -f "/home/omarci/masters/InfoShield/results/" "/home/omarci/masters/MScDissertation/results/InfoShield/allAdverts"
# Move data (LSH) from data folder
mv -f "/home/omarci/masters/MScDissertation/data/all_descriptions_full_LSH_labels.csv" "/home/omarci/masters/MScDissertation/results/InfoShield/all_descriptions_full_LSH_labels.csv"
mv -f "/home/omarci/masters/MScDissertation/data/all_descriptions_LSH_labels.csv" "/home/omarci/masters/MScDissertation/results/InfoShield/all_descriptions_LSH_labels.csv"

# 2 -> unescaped text, selected job adverts
"/home/omarci/.cache/pypoetry/virtualenvs/infoshield--uNm2Cza-py3.10/bin/python" infoshield.py "/home/omarci/masters/MScDisseration/data/merged_translated_full.csv" "id" "unescapedJobDesc"
# Move results from InfoShield
mv -f "/home/omarci/masters/InfoShield/results/" "/home/omarci/masters/MScDissertation/results/InfoShield/selectedAdverts"
# Move data (LSH) from data folder
mv -f "/home/omarci/masters/MScDissertation/data/merged_translated_full_full_LSH_labels.csv" "/home/omarci/masters/MScDissertation/results/InfoShield/selected_descriptions_full_LSH_labels.csv"
mv -f "/home/omarci/masters/MScDissertation/data/merged_translated_full_LSH_labels.csv" "/home/omarci/masters/MScDissertation/results/InfoShield/selected_descriptions_LSH_labels.csv"

# 3 -> translated text, selected job adverts
"/home/omarci/.cache/pypoetry/virtualenvs/infoshield--uNm2Cza-py3.10/bin/python" infoshield.py "/home/omarci/masters/MScDisseration/data/merged_translated_full.csv" "id" "translatedJobDesc"
# Move results from InfoShield
mv -f "/home/omarci/masters/InfoShield/results/" "/home/omarci/masters/MScDissertation/results/InfoShield/translatedAdverts"
# Move data (LSH) from data folder
mv -f "/home/omarci/masters/MScDissertation/data/merged_translated_full_full_LSH_labels.csv" "/home/omarci/masters/MScDissertation/results/InfoShield/translated_descriptions_full_LSH_labels.csv"
mv -f "/home/omarci/masters/MScDissertation/data/merged_translated_full_LSH_labels.csv" "/home/omarci/masters/MScDissertation/results/InfoShield/translated_descriptions_LSH_labels.csv"