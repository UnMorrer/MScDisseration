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
import export.save_results as save

# TODO: Create click parameter
start_page = 1

if __name__ == "__main__":
    jle.get_full_job_description(request_url="https://hu.jooble.org/jdp/7938131374549632697/Betan%C3%ADtott-k%C3%BClf%C3%B6ldi-munka-N%C3%A9metorsz%C3%A1g?ckey=NONE&rgn=4357&pos=1&elckey=774426437728287612&p=1&sid=6218519767749110609&jobAge=306&brelb=100&bscr=135214.6625088799&scr=135214.6625088799&searchTestGroup=1_2_1&iid=3556367484299631077")
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

    # TODO: Scrape new job details (full text)