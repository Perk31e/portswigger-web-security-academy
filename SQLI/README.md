# SQL Injection

| 파일 | 랩 | 취약점 | 방어 |
|------|----|--------|------|
| `blind.py`, `blind2.py` | Blind SQL injection with conditional responses | `TrackingId` 쿠키가 쿼리에 그대로 들어가고, 참/거짓에 따라 "Welcome back" 표시가 달라져 비밀번호를 한 글자씩 추출 가능 (`blind2.py`는 함수로 정리한 버전) | Prepared Statement(파라미터 바인딩) 사용 |
| `blind3_condition.py` | Blind SQL injection with conditional errors | 조건이 참일 때만 `TO_CHAR(1/0)` 에러(500)가 나도록 만들어 Oracle DB에서 비밀번호 추출 | 파라미터 바인딩, DB 에러를 사용자 응답과 분리 |
| `blind4.py` | Visible error-based SQL injection | `CAST(... AS int)` 실패 에러 메시지에 조회 결과(비밀번호)가 그대로 노출 | 파라미터 바인딩, 상세 DB 에러 메시지 비노출 |
| `blind5_time.py` | Blind SQL injection with time delays and information retrieval (파일 상단 주석에는 이전 랩 이름이 남아 있음) | `pg_sleep()` 응답 지연 여부로 참/거짓을 판단해 비밀번호 길이와 값을 추출 | 파라미터 바인딩, 쿼리 실행 시간 제한 |

- `tmp.py`: 브루트포스용 문자셋(a-z, 0-9)을 파일로 만들어 본 보조 스크립트
