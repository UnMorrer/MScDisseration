#!/usr/bin/env bash
# Bash script to run InfoShield for dissertation project

# Make folder to store results in
cd "/home/omarci/masters/MScDissertation/"
rm -rf "InfoShield"; mkdir "InfoShield"

# 1 -> unescaped text, all job adverts
"/home/omarci/.cache/pypoetry/virtualenvs/infoshield--uNm2Cza-py3.10/bin/python" "/home/omarci/masters/InfoShield/infoshield.py" "/home/omarci/masters/MScDissertation/data/all_descriptions_translated_full.csv" "id" "unescapedJobDesc"
# Move results from InfoShield
mv -f "/home/omarci/masters/MScDissertation/results/" "/home/omarci/masters/MScDissertation/InfoShield/allAdverts"
# Move data (LSH) from data folder
mv -f "/home/omarci/masters/MScDissertation/data/all_descriptions_translated_full_full_LSH_labels.csv" "/home/omarci/masters/MScDissertation/InfoShield/all_descriptions_full_LSH_labels.csv"
mv -f "/home/omarci/masters/MScDissertation/data/all_descriptions_translated_full_LSH_labels.csv" "/home/omarci/masters/MScDissertation/InfoShield/all_descriptions_LSH_labels.csv"
mv -f "/home/omarci/masters/MScDissertation/compression_rate.csv" "/home/omarci/masters/MScDissertation/InfoShield/allAdverts/compression_rate.csv"
mv -f "/home/omarci/masters/MScDissertation/template_table.csv" "/home/omarci/masters/MScDissertation/InfoShield/allAdverts/template_table.csv"

# 2 -> unescaped text, selected job adverts
"/home/omarci/.cache/pypoetry/virtualenvs/infoshield--uNm2Cza-py3.10/bin/python" "/home/omarci/masters/InfoShield/infoshield.py" "/home/omarci/masters/MScDissertation/data/merged_translated_full.csv" "id" "unescapedJobDesc"
# Move results from InfoShield
mv -f "/home/omarci/masters/MScDissertation/results/" "/home/omarci/masters/MScDissertation/InfoShield/selectedAdverts"
# Move data (LSH) from data folder
mv -f "/home/omarci/masters/MScDissertation/data/merged_translated_full_full_LSH_labels.csv" "/home/omarci/masters/MScDissertation/InfoShield/selected_descriptions_full_LSH_labels.csv"
mv -f "/home/omarci/masters/MScDissertation/data/merged_translated_full_LSH_labels.csv" "/home/omarci/masters/MScDissertation/InfoShield/selected_descriptions_LSH_labels.csv"
mv -f "/home/omarci/masters/MScDissertation/compression_rate.csv" "/home/omarci/masters/MScDissertation/InfoShield/selectedAdverts/compression_rate.csv"
mv -f "/home/omarci/masters/MScDissertation/template_table.csv" "/home/omarci/masters/MScDissertation/InfoShield/selectedAdverts/template_table.csv"

# 3 -> translated text, selected job adverts
"/home/omarci/.cache/pypoetry/virtualenvs/infoshield--uNm2Cza-py3.10/bin/python" "/home/omarci/masters/InfoShield/infoshield.py" "/home/omarci/masters/MScDissertation/data/merged_translated_full.csv" "id" "translatedJobDesc"
# Move results from InfoShield
mv -f "/home/omarci/masters/MScDissertation/results/" "/home/omarci/masters/MScDissertation/InfoShield/translatedAdverts"
# Move data (LSH) from data folder
mv -f "/home/omarci/masters/MScDissertation/data/merged_translated_full_full_LSH_labels.csv" "/home/omarci/masters/MScDissertation/InfoShield/translated_descriptions_full_LSH_labels.csv"
mv -f "/home/omarci/masters/MScDissertation/data/merged_translated_full_LSH_labels.csv" "/home/omarci/masters/MScDissertation/InfoShield/translated_descriptions_LSH_labels.csv"
mv -f "/home/omarci/masters/MScDissertation/compression_rate.csv" "/home/omarci/masters/MScDissertation/InfoShield/translatedAdverts/compression_rate.csv"
mv -f "/home/omarci/masters/MScDissertation/template_table.csv" "/home/omarci/masters/MScDissertation/InfoShield/translatedAdverts/template_table.csv"