import time

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

# Saving parameters
timestring = time.strftime("%Y%m%d")
save_folder = "/data"
save_file_name = f"JoobleData_{timestring}.csv"