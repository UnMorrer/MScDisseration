# Plan:
# Send request to get ALL jobs - DELAY of 1 sec -> 5 min scrape
# Collect UIDs: content["jobs"][x]["uid"]
# Scrape URLs for new items -> get full description
# Save all data to 3 databases (csv)
# 1. Job descriptions - most of content["jobs"][x]
# 2. Company database - content["jobs"][x]["company"] -> Collect websites as well?
# 3. Location - mostly country - is this necessary?

# New advert - scrape individual site to get FULL job ad content

# Common libraries
import random as rand
import numpy as np
import pandas as pd
import logging
import datetime
import sys
import os
import time
import requests

# Custom packages
import common.functions as func
import common.config as cfg
import scraping.jooble as jle
import export.save_results as save

# TODO: Create click parameter
start_page = 1

def scrape_jooble(start_page=1):
    """
    Function that orchestrates scraping for Jooble.hu

    Inputs:
    start_page - int: First page to request for scraping.
    Allows resuming scraping after failure
    """

    # Obtain total number of jobs on Jooble
    job_count, jobs = jle.get_jobs_from_backend(1)
    jobs_per_page = len(jobs)
    total_pages = np.ceil(job_count/jobs_per_page).astype(int)
    logging.info(f"Found {job_count} jobs on {total_pages} pages.")

    # Create result output
    dtypes = np.dtype(
        [(k, v) for k, v in cfg.data_types.items()]
    )
    all_jobs = pd.DataFrame(np.empty(0, dtype=dtypes))

    # Scrape pages
    last_uids = tuple()# tuple to keep track of UIDs encountered
    for page_num in range(start_page, total_pages+1):
        # Wait random time before every request
        time.sleep(rand.uniform(*cfg.request_delay))
        current_uids = []

        # Check if request successful
        try:
            _, jobs = jle.get_jobs_from_backend(page_num=page_num)
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
    
    # Return data after successful scrape
    logging.info(f"Finished scraping. Number of jobs scraped: ")
    return (all_jobs, # data
            0) # 0 not possible unless success since index starts with 1

if __name__ == "__main__":
    jle.get_full_job_description()

    # Logging config:
    log_name = os.getcwd() + cfg.log_dir + r'/scrape_log_' + str(datetime.date.today()) + ".txt"
    file_handler = logging.FileHandler(filename=log_name)
    stdout_handler = logging.StreamHandler(sys.stdout)
    handlers = [file_handler, stdout_handler]

    logging.basicConfig(
        level=logging.INFO, 
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s',
        handlers=handlers
    )

    # Scrape data
    job_df, last_page = scrape_jooble(start_page)

    #Save results to .csv
    append_save = False if start_page == 1 else True
    save.job_details(job_df, append=append_save)

    # TODO: Scrape new job details (full text)