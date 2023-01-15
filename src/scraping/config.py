# Scraping parameters
request_timeout = 10
request_delay = [0.25, 0.75]
# API response keys retained -> fields with info I want to use
data_types = {
    "uid": int,
    "url": str, # To scrape job description
    "isUrlHiddenFromCrawler": bool,
    "dateCaption": str, # When was entry created?
    "salary": str, # TODO: Convert
    "position": str, # job title
    "isNew": bool, # Interesting stuff
    "isPremium": bool,
    "isEasyApply": bool,
    "isRemoteJob": bool,
    "isResumeRequired": bool,
    "isAdvertLabel": bool,
    "destination": int,
    "companyIsVerified": bool,
    "companyName": str,
    "companyLink": str,
    "companyIsContactsVerified": bool,
    "companyDoesHaveHires": bool,
    "companyDoesHaveManyHires": bool,
    "companyIsActiveResponses": bool,
    "locationName": str,
    "locationIsShiftJob": bool,
    "similarGroupdId": str, #?
    "impressionId": str, #?
    "hasFewApplies": bool,
    "hasQuestions": bool,
    "tags": list, #Interesting, seems motly empty
    "highlightTags": list,
    "isDteJob": bool # Daytime?
}


# Logging parameters
log_dir = "/logs"


# Request parameters
jooble_get_url = "http://hu.jooble.org/%C3%A1ll%C3%A1s/K%C3%BClf%C3%B6ld"
jooble_post_url = "http://hu.jooble.org/api/serp/jobs"
jooble_post_headers = {
    "Accept": "/",
    "Connection": "keep-alive",
    "content-type": "application/json",
    "Host": "hu.jooble.org",
    "Origin": "https://hu.jooble.org",
    "Referer": jooble_get_url,
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fect-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
}
jooble_post_cookies = {
    "SessionCookie.hu": "-7605529932450157550*2231947513189314018*638093143747064588"
}


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