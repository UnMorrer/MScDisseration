import requests
import config
import json

# Plan:
# Send request to get ALL jobs - DELAY of 1 sec -> 5 min scrape
# Collect UIDs: content["jobs"][x]["uid"]
# Scrape URLs for new items -> get full description
# Save all data to 3 databases (csv)
# 1. Job descriptions - most of content["jobs"][x]
# 2. Company databaSE - content["jobs"][x]["company"] -> Collect websites as well?
# 3. Location - mostly country - is this necessary?

# New advert - scrape individual site to get FULL job ad content

response = requests.post(
    url=config.jooble_post_url,
    headers=config.jooble_post_headers,
    cookies=config.jooble_post_cookies,
    json=config.generate_post_request_json(1)
)

content = json.loads(response.text)
total_jobs = content["count"]
a = 1