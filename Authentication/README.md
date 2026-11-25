# Authentication

| 파일 | 랩 | 취약점 | 방어 |
|------|----|--------|------|
| `auth1.py` | Username enumeration via different responses | "Invalid username"과 "Incorrect password" 메시지가 달라 유효한 사용자명을 먼저 골라낸 뒤 비밀번호 브루트포스 | 실패 사유와 무관하게 동일한 오류 메시지, 로그인 시도 제한 |
| `auth3.py` | Password reset broken logic | 재설정 요청에서 토큰을 비워도 검증하지 않고, hidden `username` 값만 바꾸면 다른 사용자(carlos) 비밀번호 변경 가능 | 서버에서 토큰과 사용자 매핑을 검증하고, 사용 후 즉시 폐기 |
| `auth4.py`, `auth4_original.py` | Username enumeration via subtly different responses | 오류 메시지 끝의 마침표 하나 차이로 유효한 사용자명 식별 (`auth4.py`는 전수 대입, `auth4_original.py`는 메시지 빈도 비교로 찾는 정석 풀이) | 모든 실패 응답을 바이트 단위까지 동일하게 처리 |
| `auth5.py` | Username enumeration via response timing | 긴 비밀번호를 보내면 유효한 사용자일 때만 응답이 느려짐. `X-Forwarded-For`를 바꿔 IP 기반 차단도 우회 | 존재 여부와 무관하게 일정한 처리 시간, 클라이언트가 보낸 IP 헤더 불신 |
| `auth6.py` | Broken brute-force protection, IP block | 실패 횟수 카운터가 정상 로그인 한 번에 초기화되어, 2회마다 내 계정으로 로그인하며 무제한 대입 | 계정 단위 잠금, 다른 계정의 성공 로그인으로 카운터가 초기화되지 않게 설계 |
| `auth8.py` | 2FA broken logic | 2단계 인증 대상 사용자를 클라이언트 쿠키(`verify`)로 정하므로, 값을 피해자로 바꾸고 4자리 코드를 브루트포스 | 2FA 대상은 서버 세션에 저장, 코드 입력 시도 횟수 제한 |

- `username.txt`, `password.txt`: Academy가 제공하는 후보 사용자명/비밀번호 목록
- `4digit.txt`: `auth8.py`가 실행 시 자동 생성하는 0000~9999 목록이라 저장소에서는 제외
