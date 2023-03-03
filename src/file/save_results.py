# Common libraries
import logging
import os
import pandas as pd

# Custom packages
import common.config as cfg


# Save function to save results initially
def job_details(
    job_df,
    append=False,
    filename=(os.getcwd() + cfg.save_dir + "/" + cfg.save_filename + ".csv"),
    **kwargs):

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
    # Handle writing new file
    if not append:
        logging.info(f"Saving {len(job_df.index)} lines to new file...")
        job_df.to_csv(filename, mode="w", **kwargs)
        logging.info(f"Saved all items to {filename}")

    # Read in old file and only add new items (remove duplicates)
    else:
        try:
            existing_df = pd.read_csv(filename, **kwargs)
        except FileNotFoundError:
            logging.error(f"Existing data file {filename} not found.")

            new_filename = (os.getcwd() + cfg.save_dir + "/" + "Dump_" + cfg.save_filename + ".csv")

            # Try to save as new file
            job_df.to_csv(new_filename, mode="w", **kwargs)
            logging.info(f"Dumped data to file {new_filename}")

            return
        
        # Get unique UID values
        existing_uid = existing_df[cfg.unique_id_column_name].unique().tolist()
        logging.info(f"Found {len(existing_uid)} unique values already saved for today")

        # Only add new UIDs
        new_uid = job_df[cfg.unique_id_column_name].unique().tolist()

        # Select UIDs that are in new but not in existing
        add_uid = list(set(new_uid) - set(existing_uid))
        logging.info(f"Preparing to add {len(add_uid)} new values")

        # Select new rows & append
        new_rows = job_df[job_df[cfg.unique_id_column_name].isin(add_uid)]

        # Write out new rows
        new_rows.to_csv(filename, mode="a", **kwargs)
        logging.info(f"Added {len(new_rows.index)} new values to {filename}")


# Append full job text to saved data
def full_job_description():
    pass