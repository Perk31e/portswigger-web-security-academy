# OS Command Injection

| 파일 | 랩 | 취약점 | 방어 |
|------|----|--------|------|
| `os1.py` | OS command injection, simple case | 재고 조회 `storeId`가 셸 명령에 그대로 붙어 `1\|whoami` 결과가 응답에 출력 | 셸을 거치지 않는 API(인자 배열) 사용, 입력값 화이트리스트 |
| `os2.py` | Blind OS command injection with time delays | 피드백 폼 `email` 필드에 `\|\|ping -c 10 127.0.0.1\|\|`를 넣어 응답 지연(약 10초)으로 주입 확인 | 셸 호출 제거, 이메일 형식 엄격 검증 |
| `os3.py` | Blind OS command injection with output redirection | 출력이 안 보이므로 `whoami>/var/www/images/output.txt`로 쓰고 이미지 경로로 읽어 옴 | 셸 호출 제거, 웹 서버 계정의 웹 루트 쓰기 권한 최소화 |
