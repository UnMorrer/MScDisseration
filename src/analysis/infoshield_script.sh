#!/usr/bin/env bash
# Bash script to run InfoShield for dissertation project

# 1 -> unescaped text, all job adverts
"/home/omarci/.cache/pypoetry/virtualenvs/infoshield--uNm2Cza-py3.10/bin/python" infoshield.py "/home/omarci/masters/MScDisseration/data/all_descriptions.csv" "id" "unescapedJobDesc"
# 2 -> unescaped text, selected job adverts
"/home/omarci/.cache/pypoetry/virtualenvs/infoshield--uNm2Cza-py3.10/bin/python" infoshield.py "/home/omarci/masters/MScDisseration/data/merged_translated_full.csv" "id" "unescapedJobDesc"
# 3 -> translated text, selected job adverts
"/home/omarci/.cache/pypoetry/virtualenvs/infoshield--uNm2Cza-py3.10/bin/python" infoshield.py "/home/omarci/masters/MScDisseration/data/merged_translated_full.csv" "id" "translatedJobDesc"