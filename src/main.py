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
import click

# Custom packages
import common.config as cfg
import scraping.jooble as jle
import file.save_results as save
import file.load_results as load


@click.command()
@click.option("-sp", "--start-page", default=392, help="Start page of backend scraping")
@click.option("-ufp", "--url-file-path", default="", help="File path for detailed scraping URLs")
def main(start_page, url_file_path):
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

    if url_file_path == "":
        # Scrape data
        job_df, last_page = jle.scrape_jooble_backend(start_page)

        #Save results to .csv
        append_save = False if start_page == 1 else True
        save.job_details(job_df, append=append_save)

        # Load previous job data
        previous_ids = load.load_previous_data(
            cfg.save_dir,
            filename_regex=cfg.load_match_regex
        )[cfg.unique_id_column_name]

        # Scrape full details for new jobs
        unscraped, full_details_df = jle.get_all_full_job_descriptions(
            job_df,
            previous_ids=previous_ids
            )
    
    else:
         # Jump straight to detailed scraping upon failure

        # Load URLs into list:
        with open(url_file_path, "r") as file:
             urls = [line.rstrip() for line in file]   

        unscraped, full_details_df = jle.get_all_full_job_descriptions(
            url_list=urls
            )
    
    save.job_details(
        full_details_df,
        append=append_save,
        filename=(os.getcwd() + cfg.save_dir + "/" + cfg.full_desc_filename + ".csv")
    )

    # Save unscraped URLs if any left
    if len(unscraped) > 0:
        with open(f"{cfg.save_dir}/unscraped_details_{cfg.timestring}.txt", 'w') as file:
                for row in unscraped:
                    s = ",\n".join(map(str, row))
                    file.write(s+'\n')

if __name__ == "__main__":
    main()