import requests
import scraping.config as cfg
import json


def get_jobs_from_backend(
                          page_num,
                          request_url=cfg.jooble_post_url,
                          request_headers=cfg.jooble_post_headers,
                          request_cookies=cfg.jooble_post_cookies,
                          request_json=cfg.generate_post_request_json
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

    content = json.loads(response.text)

    job_count = content["count"]
    job_details = content["jobs"]

    return job_count, job_details