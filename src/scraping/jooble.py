import requests
import common.config as cfg
import json


def generate_post_request_json(page_num):
    """
    Function to generate dictionary to send to
    Jooble in a HTTPS POST request.
    
    Inputs:
    page_num - int: Page number for request
    
    Returns:
    request - dict: Request headers"""

    jooble_post_json = {
        "coords": None,
        "isCityregion": False,
        "isRemoteSerp": False,
        "jobTypes": [],
        "page": page_num,
        "region": "Külföld",
        "regionId": 4357,
        "search": "",
    }
    return jooble_post_json


def get_jobs_from_backend(
                          page_num,
                          request_url=cfg.jooble_post_url,
                          request_headers=cfg.jooble_post_headers,
                          request_cookies=cfg.jooble_post_cookies,
                          request_json=generate_post_request_json
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

    # Raise error for HTTP code other than 200
    response.raise_for_status()

    content = json.loads(response.text)

    job_count = content["count"]
    job_details = content["jobs"]

    return job_count, job_details


def get_full_job_description(
    request_url=cfg.jooble_post_url,
    request_headers=cfg.jooble_get_headers,
    request_cookies=cfg.jooble_post_cookies,
    html_tag=None):
    
    """
    Function to get full job description from jooble.hu.

    Inputs:

    Returns:

    """

    response = requests.get(request_url)
    return None