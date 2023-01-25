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
import scraping.config as cfg
import scraping.jooble as jle
import export.save_results as save

def scrape_jooble():
    """
    Function that orchestrates scraping for Jooble.hu
    """

    # Obtain total number of jobs on Jooble
    job_count, jobs = jle.get_jobs_from_backend(1)
    jobs_per_page = len(jobs)
    total_pages = np.ceil(job_count/jobs_per_page).astype(int)
    logging.info(f"Found {job_count} jobs on {total_pages} pages.")

    # Scrape pages
    for page_num in range(1, total_pages+1):
        # Wait random time before every request
        time.sleep(rand.uniform(*cfg.request_delay))

        # Check if request successful
        try:
            _, jobs = jle.get_jobs_from_backend(page_num=page_num)
        except requests.HTTPError:
            # Save progress into a file
            pass
            #TODO: save_output()

        unpacked_jobs = [func.flatten_dict(job) for job in jobs]

        # TODO: Save progress & allow to resume if scraping fails midway through
        all_jobs += unpacked_jobs

    # Plan:
    # Send request to get ALL jobs - DELAY of 1 sec -> 5 min scrape
    # Collect UIDs: content["jobs"][x]["uid"]
    # Scrape URLs for new items -> get full description
    # Save all data to 3 databases (csv)
    # 1. Job descriptions - most of content["jobs"][x]
    # 2. Company database - content["jobs"][x]["company"] -> Collect websites as well?
    # 3. Location - mostly country - is this necessary?

# New advert - scrape individual site to get FULL job ad content

if __name__ == "__main__":
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

    # Custom functions
    scrape_jooble()