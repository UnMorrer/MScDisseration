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
    "SessionCookie.hu": "341781737510320955*5073937324693764649*638133978449820667"
}

# GET request for full details
jooble_get_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.5",
    "Connection": "keep-alive",
    "Host": "hu.jooble.org",
    "Origin": "https://hu.jooble.org",
    "Cookie": """@key@=1; TrafficSource=262145*0; SessionCookie.hu=341781737510320955*5073937324693764649*638133978449820667; SessionUtmCookie.hu=; xtest_620_1=2; LastVisit=2/28/2023 7:55:20 PM; sever=35; .AspNetCore.Session=CfDJ8H+K1ENDEvVDhhoVDlz6SYkF/2XBRJ5kAiyZxMQrB9IELAbY0E3JkN6vxc3Ls6aAs/sZqOOt480ObVKSxhFNFmjju+EWfHxPFC7fRuO9Zandyyucgg0ItWYm/cfr407cwAOgqyL8nIWGuj7TQ9ITQCDBz0xyo212QQ4ishfShx1S; shistory=%5b%7b%22sid%22%3a-8319916264116130067%2c%22ct%22%3a%222023-02-28T19%3a17%3a21.7043458%22%2c%22qh%22%3a0%2c%22rs%22%3a%22K%c3%bclf%c3%b6ld%22%2c%22ss%22%3a%22%22%7d%5d; cregion=4357; ver=desktop; AuthId=4106940555895744975; CookieScriptConsent={"googleconsentmap":{"ad_storage":"targeting","analytics_storage":"performance","functionality_storage":"functionality","personalization_storage":"functionality","security_storage":"functionality"},"action":"reject","categories":"[]","key":"cc8365db-45a2-430b-99b9-c5f063803c7b"}; ShouldShowSubscribeTooltip=1; ULang=0; uuid=-2398575995389841143; user_bucket=1; rk_groups=; g_state={"i_p":1677614679533,"i_l":1}; ssearchstring=; ts-consent={"date":"2023-02-28T18:10:20.018Z"}; datadome=0FzTOPK7-9E0m-wh9Xng_Ai74iylKvTVGAG4ccdbAzFc7A0LXi5PR9LoWnvCJfx92mkIDEySd9yq73vf1ieGTvLQw6s~8~E1z7e~BcU8J7kvmezm-SPvSbv5En_QnPz4; REGION_TOOLTIP_COOKIE=1""",
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
full_desc_filename = f"JoobdleData_FullDesc_{timestring}"
unique_id_column_name = "uid"

# Load parameters
load_match_regex = fr"^JoobleData_FullDesc_{timestring}.csv$"
external_site_url = "https://hu.jooble.org/away/"

# Finding new jobs that haven't been scraped yet
link_colname = "url"