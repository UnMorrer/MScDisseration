def main():
    """
    Function that executes scraping
    """

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
    main()