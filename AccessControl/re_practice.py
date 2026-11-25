import re

'''
• \w → "영문, 숫자, _ 중 아무거나 한 글자
• \d → 숫자 한 글자 (0~9)
• \s → 공백 한 글자 (스페이스, 탭, 줄바꿈)
• . → 줄바꿈 빼고 아무 글자 한 개
• [abc] → a, b, c 중 하나 / [a-z0-9] → 소문자나 숫자 중 하나
• [^"] → "만 빼고 아무 글자 (^가 대괄호 안 맨 앞에 오면 "제외")
• 대문자 버전은 반대예요: \D 숫자가 아닌 것, \W 단어 글자가 아닌 것, \S 공백이 아닌 것

반복 기호ㅉ
• + → 1개 이상
• * → 0개 이상 (없어도 됨)
• ? → 0개 또는 1개
• {4} → 정확히 4개 / {2,5} → 2~5개
'''

t = 'pin=0427 key=ab-12_cd'
print(re.search(r'pin=(\d+)', t).group())       # pin=0427
print(re.search(r'pin=(\d+)', t).group(1))      # 0427
print(re.search(r'key=(\w+)', t).group(1))      # ab   ("-"" 에서 멈춤 -> \w에 "-"는 포함되지 않으니까)
print(re.search(r'key=(\S+)', t).group(1))      # ab-12_cd
print(re.search(r'key=([^ ]+)', t).group(1))    # ab-12_cd