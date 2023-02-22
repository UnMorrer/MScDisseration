# Common libraries
import requests
import common.config as cfg
import json
import bs4
import logging
import time
import numpy as np
import pandas as pd
import random as rand

# Custom packages
import common.functions as func
import common.scraping as scrape_utils

def generate_post_request_json(page_num):
    """
    Function to generate dictionary to send to
    Jooble in a HTTPS POST request.
    
    Inputs:
    page_num - int: Page number for request
    
    Returns:
    request - dict: Request headers"""

    jooble_post_json = {
        "coords": None,
        "isCityregion": False,
        "isRemoteSerp": False,
        "jobTypes": [],
        "page": page_num,
        "region": "Külföld",
        "regionId": 4357,
        "search": "",
    }
    return jooble_post_json


def get_jobs_from_backend(
                          page_num,
                          request_url=cfg.jooble_post_url,
                          request_headers=cfg.jooble_post_headers,
                          request_cookies=cfg.jooble_post_cookies,
                          request_json=generate_post_request_json
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

    # Raise error for HTTP code other than 200
    response.raise_for_status()

    content = json.loads(response.text)

    job_count = content["count"]
    job_details = content["jobs"]

    return job_count, job_details


def scrape_jooble_backend(start_page=1):
    """
    Function that orchestrates scraping for Jooble.hu

    Inputs:
    start_page - int: First page to request for scraping.
    Allows resuming scraping after failure
    """

    # Obtain total number of jobs on Jooble
    job_count, jobs = get_jobs_from_backend(1)
    jobs_per_page = len(jobs)
    total_pages = np.ceil(job_count/jobs_per_page).astype(int)
    logging.info(f"Found {job_count} jobs on {total_pages} pages.")

    # Create result output
    all_jobs = func.create_dataframe_with_dtypes(cfg.data_types)

    # Scrape pages
    last_uids = tuple()# tuple to keep track of UIDs encountered
    for page_num in range(start_page, total_pages+1):
        # Wait random time before every request
        time.sleep(rand.uniform(*cfg.request_delay))
        current_uids = []

        # Check if request successful
        try:
            _, jobs = get_jobs_from_backend(page_num=page_num)
        except requests.HTTPError as e:
            # Handle unsuccessful request
            logging.error(f"HTTP {e.response.status_code} error encountered during scraping")
            logging.info(f"Scraping aborted on page {page_num}")
            return (all_jobs, #data
                    page_num) # last page retrieved
        # Keep only data for relevant keys (columns)
        for job in jobs:
            flattened_job = func.flatten_dict(job)
            filtered_job = pd.Series(flattened_job)[cfg.data_types.keys()]

            # Check if results are different
            if filtered_job["uid"] in last_uids:
                logging.warning(
                    f"Same UID encountered twice during scraping: {filtered_job['uid']}")
            
            # Add to track current uid
            current_uids.append(filtered_job["uid"])

            # Add new row to results
            all_jobs = pd.concat([all_jobs, filtered_job],
                                 ignore_index=True)
        
        # Reset UIDs after extraction
        last_uids = tuple(current_uids)


def get_full_job_description(
    request_url,
    request_headers=cfg.jooble_get_headers,
    selector_type=cfg.full_content_selector_type,
    selector_params=cfg.full_content_selector_params,
    content_rename_keys=cfg.full_content_renaming,
    content_data_names=cfg.full_content_data_types.keys()):
    
    """
    Function to get full job description from jooble.hu.

    Inputs:
    request_url - str: The URL of the requested job
    request_headers - dict: Headers to send with
    the GET request.
    selector_type - str: Selector to find job
    description HTML tag.
    selector_params - dict: Parameters to find
    the HTML tag of job descriptions.
    content_rename_keys - dict(str): Dictionary
    with old names as keys and new names as values.
    Used to rename JSON dictionary keys retrieved.
    save_key_names - list(str): A list of strings
    that contain dictionary keys that will be saved
    /retrieved by the script.

    Returns:
    job_details - pd.Series: A Pandas series 
    with individual job details.
    """

    response = requests.get(
        request_url,
        headers=request_headers)

    # Check request is OK
    response.raise_for_status()

    # Begin parsing
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    script_block = soup.find(
        selector_type,
        selector_params
    )

    # Strip details from contents
    details_dict = json.loads(script_block.contents[0])

    # Flatten details_dict
    details_flat_dict = func.flatten_dict(details_dict, parent_key="job")

    # Rename some keys
    for old_key, new_key in content_rename_keys.items():
        try:
            details_flat_dict[new_key] = details_flat_dict.pop(old_key)
        except KeyError: # Catch fields not existing in job description
            details_flat_dict[new_key] = None
    
    # Ensure all values are available - impute missing as None
    for key in content_data_names:
        if key not in details_flat_dict.keys():
            details_flat_dict[key] = None

    # Unescape HTML encoding for job description
    job_description = details_flat_dict[cfg.job_full_details_column]
    cleaned_job_description = scrape_utils.html_to_text(job_description)
    details_flat_dict[cfg.cleaned_job_full_details_column] = cleaned_job_description

    # Create pandas Series to return
    job_details = pd.Series(details_flat_dict)[content_data_names]

    return job_details