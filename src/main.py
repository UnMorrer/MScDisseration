# Common libraries
import random as rand
import numpy as np
import pandas as pd

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
    job_count, _ = jle.get_jobs_from_backend(1)

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
    scrape_jooble()