import requests
import config
import json


def get_jobs_from_backend(
                          page_num,
                          request_url=config.jooble_post_url,
                          request_headers=config.jooble_post_headers,
                          request_cookies=config.jooble_post_cookies,
                          request_json=config.generate_post_request_json
                          ):
    """
    Function to get job information from backend API

    Inputs:
    page_num - int: Page number of job advert to scratch

    Returns:
    job_count - int: Total number of jobs
    job_details - dict: Dictionary holding job details
    """

    response = requests.post(
        url=request_url,
        headers=request_headers,
        cookies=request_cookies,
        json=request_json(page_num)
    )

    content = json.loads(response.text)

    job_count = content["count"]
    job_details = content["jobs"]

    return job_count, job_details


# Plan:
# Send request to get ALL jobs - DELAY of 1 sec -> 5 min scrape
# Collect UIDs: content["jobs"][x]["uid"]
# Scrape URLs for new items -> get full description
# Save all data to 3 databases (csv)
# 1. Job descriptions - most of content["jobs"][x]
# 2. Company database - content["jobs"][x]["company"] -> Collect websites as well?
# 3. Location - mostly country - is this necessary?

# New advert - scrape individual site to get FULL job ad content

content = json.loads(response.text)
total_jobs = content["count"]
a = 1