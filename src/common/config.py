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
    "SessionCookie.hu": "5150933470332396708*7876963493565951500*638176618779923633"
}

# GET request for full details
jooble_get_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.5",
    "Connection": "keep-alive",
    "Host": "hu.jooble.org",
    "Origin": "https://hu.jooble.org",
    "Cookie": r"""datadome=1cEx_Bu8lhs-YtZwTlo6144GPcaCiA6ej75trvziVi5BufUCwC8uMyWabe7pjr53Ya1NO--~wZ_Q7mgzsQ8pY78_Z19U_udLqEGlzgxQg3_GRRdLSauyf74y7CXQ7EPx; SessionCookie.hu=6823161071285596860*83310121684355370*638183499489399792; SessionUtmCookie.hu=; TrafficSource=262145*0; user_bucket=12; LastVisit=4/29/2023 8:25:46 AM; uuid=-2586974009364788227; rk_groups=; sever=35; ULang=0; ver=desktop; .AspNetCore.Session=CfDJ8BTj75HgVZdJpis1gEsSmG2Ew7MyJqfG1M+OImFfOeZTPow70BShFlpSXb1g8Wk98p5RvHVhzKeT53WRy3coShhxnZBTXcifDkOFjsql3du1wNNH4cv1byTnguEFSqPO/yciT+jkNipiapYyDzqsQEcWDXcUo5Tye+j3ZZKDDHY4""",
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