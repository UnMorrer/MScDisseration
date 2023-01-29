# Common libraries
import logging
import os

# Custom packages
import common.config as cfg


# Save function to save results initially
def job_details(
    job_df,
    append=False,
    filename=(os.getcwd() + cfg.save_dir + "/" + cfg.save_filename + ".csv"),
    kwargs=None):

    """
    Function to save initial API scraping results to disk

    Inputs:
    job_df - DataFrame: Job details defined in config
    append - bool: Whether to append to existing 
    data saved (used on scraping failure)
    filename - str: Name (and folder) used for output file
    kwargs - dict: Additional keyword arguments to be passed 
    down to pandas.DataFrame.to_csv() method

    Returns:
    None
    """
    filemode = "a" if append else "w"

    job_df.to_csv(filename, mode=filemode, **kwargs)
    logging.info(f"Saved {len(job_df.index)} lines to {filename}")


# TODO: Allow continuation mid-way (scraping failure)

# Append full job text to saved data
def job_full_description():
    pass