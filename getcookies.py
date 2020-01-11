import json

def getcookies():
    cookies = {}

    cookies_edit = json.load(open("cookies.txt","r"))

    for cookie in cookies_edit:
        cookies[cookie["name"]] = cookie["value"]

    return cookies

