import time

# Scraping parameters
request_timeout = 10
request_delay = [2, 5]
detailed_request_delay = [5, 15]
max_unsuccessful_requests = 5
max_request_page_num = 51 # No jobs retrieved after page 51

# API response keys retained -> fields with info I want to use
data_types = {
    "uid": int,
    "url": str, # To scrape job description
    "isUrlHiddenFromCrawler": bool,
    "dateCaption": str, # When was entry created?
    "salary": str, # TODO: Convert
    "content": str, # Advert text (first n characters)
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
    "impressionId": str, # ?
    "similarGroupId": str, # ?
    "locationName": str, # Country
    "locationIsShiftJob": bool,
    "hasFewApplies": bool,
    "hasQuestions": bool,
    "tags": list, #Interesting, seems mostly empty
    "highlightTags": list,
    "isDteJob": bool, # Daytime?
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
jooble_post_json = {
        "coords": None,
        "date": 8, #Last 24 hours
        "isCityregion": False,
        "isRemoteSerp": False,
        "jobTypes": [],
        "region": "Külföld",
        "regionId": 4357,
        "search": "",
}
jooble_post_cookies = {
    "SessionCookie.hu": "2721217798599165519*-3944139081951626828*638159301588299143"
}

# GET request for full details
jooble_get_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.5",
    "Connection": "keep-alive",
    "Host": "hu.jooble.org",
    "Origin": "https://hu.jooble.org",
    "Cookie": """@key@=1; SessionCookie.hu=2721217798599165519*-3944139081951626828*638159301588299143; SessionUtmCookie.hu=; TrafficSource=262145*0; user_bucket=5; xtest_628_0=2; rk_groups=; sever=35; ULang=0; .AspNetCore.Session=CfDJ8BTj75HgVZdJpis1gEsSmG0CHJqEBNWi/C7RYx5GwynXNubke8ELQL6KqbYxKCgtMQKAd2BEITsGlZM3TQMzQa81ja3OgExQfEpWVbkJKh9U3UkFnE5epoGW6mwHfW7/ZjCXz+L65yBt/X/QKz0XWhoZSeEOJ804DVCteRiv14Ll; AuthId=-8290964824920865415; g_state={"i_p":1680340447031,"i_l":1}; CookieScriptConsent={"action":"reject","categories":"[]","key":"4403825f-d2a3-4a2a-a73f-4306730d12fa"}; datadome=3n7mcTDsGqm1rYlgdyIl3-DRb1ipvgK49ggkXpDuEAD1I~09Q1ocGF0GHvYqRzFtn7noK9nRwogQFnt94plyvoruCkQbmqniO3HrB2jhgOndJ1HV~GHCzNG4jXdHhyj1""",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0",
}
full_content_selector_type = "script"
full_content_selector_params = {
    "type": "application/ld+json",
}

full_content_renaming = {
    "jobBaseSalaryValueUnitText": "jobBaseSalaryTimeUnit",
    "jobIdentifierValue": "uid",
}

full_content_data_types = {
    "uid": str,
    "jobTitle": str, 
    "jobDescription": str, # sanity check: must equal position
    "jobDatePosted": str,
    "jobHiringOrganizationName": str,
    "jobHiringOrganizationSameAs": str, #Seems like web address
    "jobBaseSalaryCurrency": str,
    "jobBaseSalaryValueMinValue": float,
    "jobBaseSalaryValueMaxValue": float,
    "jobBaseSalaryTimeUnit": str,
}

job_full_details_column = "jobDescription" # TODO: Used for cleaning later
cleaned_job_full_details_column = "jobDescriptionClean"

# Saving parameters
timestring = time.strftime("%Y%m%d")
save_dir = "/data"
save_filename = f"JoobleData_{timestring}"
full_desc_filename = f"JoobleData_FullDesc_{timestring}"
unique_id_column_name = "uid"

# Load parameters
load_match_regex = fr"^JoobleData_FullDesc_{timestring}.csv$"
external_site_url = "https://hu.jooble.org/away/"

# Finding new jobs that haven't been scraped yet
link_colname = "url"