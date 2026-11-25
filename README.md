# PortSwigger Web Security Academy 실습 기록

PortSwigger Web Security Academy의 필수 10개 유닛 실습 랩을 **Burp Suite로 요청을 분석**하고, 같은 공격 흐름을 **Python `requests` 스크립트로 재현**한 기록입니다.
각 스크립트에는 단계별(`[step1]`, `[step2]` …) 공격 과정과, 그때 실제로 받은 서버 응답을 주석으로 남겨 두었습니다.

## 진행 방식

1. 랩을 열고 Burp Proxy / Repeater로 정상 요청과 응답을 관찰합니다.
2. 취약 지점을 찾고 Repeater에서 페이로드를 직접 검증합니다.
3. 검증한 흐름을 `requests.Session()` 기반 스크립트로 옮겨, 로그인부터 공격 성공까지 한 번에 재현합니다.
4. 브루트포스, 블라인드 추출처럼 반복이 많은 단계는 반복문이나 `ThreadPoolExecutor`로 자동화합니다.

## 유닛별 요약

| # | 유닛 | 폴더 | 랩 수 | 핵심 기법 |
|---|------|------|:---:|-----------|
| 1 | SQL Injection | [`SQLI/`](SQLI/) | 4 | 조건 응답, 조건 에러, 에러 메시지 노출, 시간 지연 기반 블라인드 SQLi로 관리자 비밀번호 추출 |
| 2 | Authentication | [`Authentication/`](Authentication/) | 6 | 응답 차이·응답 시간 기반 사용자 열거, IP 차단 우회 브루트포스, 비밀번호 재설정 로직 결함, 2FA 로직 결함 |
| 3 | Path Traversal | [`Path Traversal/`](Path%20Traversal/) | 6 | `../`, 절대경로, `....//`, 이중 URL 인코딩, 시작 경로 검증 우회, 널바이트 확장자 우회 |
| 4 | OS Command Injection | [`OS Command Injection/`](OS%20Command%20Injection/) | 3 | 직접 출력, 시간 지연(blind), 출력 리다이렉션(blind) |
| 5 | Access Control | [`AccessControl/`](AccessControl/) | 12 | 숨겨진 관리자 경로, 쿠키·파라미터 기반 권한 조작, IDOR, `X-Original-Url`, 메서드 변경, 다단계 처리, Referer 기반 접근 통제 우회 |
| 6 | File Upload | [`File Upload Vulnerabilities/`](File%20Upload%20Vulnerabilities/) | 6 | 웹셸 업로드, Content-Type 우회, 파일명 경로 조작, `.htaccess` 업로드, 널바이트 확장자, PNG 폴리글롯 |
| 7 | SSRF | [`SSRF/`](SSRF/) | 4 | 로컬 서버·내부망 스캔, 블랙리스트 필터 우회(`127.1`, 이중 인코딩), 오픈 리다이렉트 연계 |
| 8 | CSRF | [`CSRF/`](CSRF/) | 2 | 방어 없는 CSRF, 요청 메서드에 따라 토큰 검증이 빠지는 경우 |
| 9 | XSS | [`XSS/`](XSS/) | 8 | Reflected / Stored / DOM XSS, HTML·속성·JavaScript 문자열 컨텍스트 탈출 |
| 10 | API Testing | [`API Testing/`](API%20Testing/) | 3 | API 문서 노출, 숨은 HTTP 메서드(PATCH) 악용, Mass Assignment |

유닛별 랩 이름, 취약점, 방어 방법은 각 폴더의 `README.md`에 정리했습니다.

## 실행 방법

```bash
pip install requests
python "SQLI/blind2.py"
```

- 각 스크립트 상단의 `base` / `URL` 값은 제가 풀 때 발급받은 랩 인스턴스 주소이고, 지금은 만료되었습니다. 직접 실행하려면 새로 연 랩 주소로 바꿔야 합니다.
- 코드 안의 `session` 쿠키, API Key, 비밀번호 등은 모두 PortSwigger 랩이 제공한 일회성 값이며 실제 계정 정보가 아닙니다.
- `wiener:peter`, `carlos`, `administrator`는 Academy 랩의 기본 테스트 계정입니다.

## 사용 도구

- Burp Suite (Proxy, Repeater, Intruder)
- Python 3, `requests`
- [SecLists](https://github.com/danielmiessler/SecLists) `LFI-Jhaddix.txt` (Path Traversal 퍼징)
- ExifTool (PNG 폴리글롯 웹셸 제작)

## 주의

모든 코드는 PortSwigger가 학습용으로 제공한 랩 환경에서만 사용했습니다. 허가받지 않은 시스템에 사용하는 것은 불법입니다.
