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
    "SessionCookie.hu": "-3141350288078534096*-1894521335442483615*638133982687416104"
}

# GET request for full details
jooble_get_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.5",
    "Connection": "keep-alive",
    "Host": "hu.jooble.org",
    "Origin": "https://hu.jooble.org",
    "Cookie": """@key@=1; datadome=1XhoK-xWNa_TiHyDP-VI3u3B8F9EIGsGcQ51O08BxV3Xdh~hnybkRChB9vRyNltCB8LTG03SH2WAIBW~w3PGcESO4_k5c4Cy2jHhy9SH60GeM6lHtocdVu0I0W7uyJFY; SessionCookie.hu=-3141350288078534096*-1894521335442483615*638133979184073046; SessionUtmCookie.hu=; TrafficSource=262145*0; user_bucket=8; xtest_620_1=1; LastVisit=3/2/2023 11:30:48 PM; uuid=-4683418874738951125; rk_groups=; sever=35; ULang=0; ver=desktop; .AspNetCore.Session=CfDJ8H+K1ENDEvVDhhoVDlz6SYnJLLPl/SEkneBStRGoOT/oIGF6RwtfqMjbWJ7PgLf8EpKIBacKv0Uw3P0kgd0pNTETLD0hmy6wEkuUjDx2cnEHqD1g8Wkvu9QIKN1XMyAIgQOL2jr1B5bpjviowFDON32F9nWIHgxyr6yBa0mjXe2n; shistory=%5b%7b%22sid%22%3a-684900947169425579%2c%22ct%22%3a%222023-03-03T00%3a46%3a06.5875256%22%2c%22qh%22%3a3104217258921474684%2c%22rs%22%3a%22N%c3%a9metorsz%c3%a1g%22%2c%22ss%22%3a%22%c3%a1pol%c3%b3%2fn%c5%91%22%7d%2c%7b%22sid%22%3a-1894521335442483615%2c%22ct%22%3a%222023-03-03T00%3a45%3a54.6534976%22%2c%22qh%22%3a3104217258921474684%2c%22rs%22%3a%22Ausztria%22%2c%22ss%22%3a%22%c3%a1pol%c3%b3%2fn%c5%91%22%7d%2c%7b%22sid%22%3a-1894521335442483615%2c%22ct%22%3a%222023-03-03T00%3a45%3a42.591424%22%2c%22qh%22%3a-1347383144879237843%2c%22rs%22%3a%22N%c3%a9metorsz%c3%a1g%22%2c%22ss%22%3a%22szak%c3%a1cs+(lindau)%22%7d%2c%7b%22sid%22%3a-684900947169425579%2c%22ct%22%3a%222023-03-03T00%3a45%3a31.8369109%22%2c%22qh%22%3a6561976692916208317%2c%22rs%22%3a%22N%c3%a9metorsz%c3%a1g%22%2c%22ss%22%3a%22%c3%a9p%c3%adt%c5%91ipari+%c3%a1ll%c3%a1sok+n%c3%a9met+munka%22%7d%2c%7b%22sid%22%3a-684900947169425579%2c%22ct%22%3a%222023-03-02T23%3a57%3a38.8169789%22%2c%22qh%22%3a2965869984407056623%2c%22rs%22%3a%22Lengyelorsz%c3%a1g%22%2c%22ss%22%3a%22remote+mid+product+owner+%40+pragmago.tech%22%7d%2c%7b%22sid%22%3a-684900947169425579%2c%22ct%22%3a%222023-03-02T23%3a57%3a35.9636158%22%2c%22qh%22%3a-3565971998196271557%2c%22rs%22%3a%22Lengyelorsz%c3%a1g%22%2c%22ss%22%3a%22mid+%2f+senior+business+and+system+analyst+%40+pragmago.tech%22%7d%2c%7b%22sid%22%3a-684900947169425579%2c%22ct%22%3a%222023-03-02T23%3a37%3a01.7755176%22%2c%22qh%22%3a-2666412276401874684%2c%22rs%22%3a%22Kanada%22%2c%22ss%22%3a%22min%c5%91s%c3%a9gellen%c5%91rz%c5%91%22%7d%2c%7b%22sid%22%3a-684900947169425579%2c%22ct%22%3a%222023-03-02T23%3a35%3a36.8645909%22%2c%22qh%22%3a5055904074751898315%2c%22rs%22%3a%22N%c3%a9metorsz%c3%a1g%22%2c%22ss%22%3a%22offenburg%2c+n%c3%a9metorsz%c3%a1g+-+betan%c3%adtott+h%c3%basipari+csomagol%c3%b3%22%7d%5d; ssearchstring=%c3%a1pol%c3%b3%2fn%c5%91; cregion=4384; AuthId=4833391428735769071; REGION_TOOLTIP_COOKIE=1""",
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