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
import logging
import datetime
import sys
import os

# Custom packages
import common.config as cfg
import scraping.jooble as jle
import file.save_results as save

# TODO: Create click parameter
start_page = 1

if __name__ == "__main__":
    a = jle.get_full_job_description(request_url=r"https://hu.jooble.org/desc/141750743977837784?ckey=betan%c3%adtott+k%c3%bclf%c3%b6ldi+munka&rgn=4384&pos=1&elckey=-2011316934996023714&p=1&sid=4738959385858235377&jobAge=302&brelb=100&bscr=27.833&scr=27.833&searchTestGroup=1_2_1&iid=-8955806754543657294")
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
    job_df, last_page = jle.scrape_jooble_backend(start_page)

    #Save results to .csv
    append_save = False if start_page == 1 else True
    save.job_details(job_df, append=append_save)

    # Find new job IDs

    # TODO: Scrape full job advert
    # Text -> {job_id}.txt
    # Look for files/IDs not already in folder