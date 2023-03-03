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
    "SessionCookie.hu": "-7271910383396867134*-6430216621463625115*638134691081316147"
}

# GET request for full details
jooble_get_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.5",
    "Connection": "keep-alive",
    "Host": "hu.jooble.org",
    "Origin": "https://hu.jooble.org",
    "Cookie": """SessionCookie.hu=-7271910383396867134*-6430216621463625115*638134691081316147; SessionUtmCookie.hu=; TrafficSource=262145*0; xtest_620_1=2; LastVisit=3/3/2023 9:14:32 AM; sever=35; ver=desktop; .AspNetCore.Session=CfDJ8H+K1ENDEvVDhhoVDlz6SYlFKAOvQICOxmUH3BuW013i78DH5eKfk2MMFoFdKaEcyvnTo6ULdcET2THRCVFzFPhjDF9X7nD3VtgBtOekAUPkXBptOGD309sDKyC7FuZkLeB55hJFAnWo2BoVe1RKlAKt13OBNigYaXuw16l7CTta; CookieScriptConsent={"googleconsentmap":{"ad_storage":"targeting","analytics_storage":"performance","functionality_storage":"functionality","personalization_storage":"functionality","security_storage":"functionality"}}; AuthId=8692201674252901183; shistory=%5b%7b%22sid%22%3a-2804161527258974636%2c%22ct%22%3a%222023-03-03T09%3a14%3a39.2643253%22%2c%22qh%22%3a0%2c%22rs%22%3a%22K%c3%bclf%c3%b6ld%22%2c%22ss%22%3a%22%22%7d%5d; cregion=4357; datadome=1eCIqQVns3tqfbyhUhfq95amZWrjUzXEXzOFuLSawnWOMzdZEb0wVEvrcegQVff5B1OPzriuUMT_7jM8cCXl_36rOCx8T9V7nYlGkZ6Jl1wCVzbtBWR6s7u8dRVGbKnR; REGION_TOOLTIP_COOKIE=1; ULang=0; uuid=-616880823557514746"""
    "Referer": jooble_get_url,
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
full_desc_filename = f"JoodleData_FullDesc_{timestring}"
unique_id_column_name = "uid"

# Load parameters
load_match_regex = fr"^JoobleData_FullDesc_{timestring}.csv$"
external_site_url = "https://hu.jooble.org/away/"

# Finding new jobs that haven't been scraped yet
link_colname = "url"