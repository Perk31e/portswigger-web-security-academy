# Access Control

| 파일 | 랩 | 취약점 | 방어 |
|------|----|--------|------|
| `ac1.py` | Unprotected admin functionality | `robots.txt`에 관리자 경로가 노출되고, 해당 경로에 인증이 없음 | 모든 관리 기능에 서버 측 권한 검사 |
| `ac2.py` | Unprotected admin functionality with unpredictable URL | 예측하기 어려운 관리자 경로가 클라이언트 JS에 그대로 노출 | 경로 숨기기에 의존하지 말고 서버 측 권한 검사 |
| `ac3.py` | User role controlled by request parameter | `Admin=true` 쿠키만으로 관리자 권한 부여 | 권한은 서버 세션에 저장, 클라이언트 값 불신 |
| `ac4.py` | User role can be modified in user profile | 이메일 변경 JSON에 `roleid: 2`를 추가하면 권한까지 변경 | 수정 가능한 필드를 화이트리스트로 제한 |
| `ac5.py` | User ID controlled by request parameter | `id` 파라미터를 바꾸면 다른 사용자의 API Key 조회 (IDOR) | 요청한 리소스의 소유자가 세션 사용자와 같은지 확인 |
| `ac6.py` | User ID controlled by request parameter, with unpredictable user IDs | 게시글 작성자 링크에서 피해자 GUID가 노출되어 IDOR 가능 | GUID와 상관없이 소유권 검사 |
| `ac7.py` | User ID controlled by request parameter with data leakage in redirect | 권한이 없을 때 302 리다이렉트하면서 응답 본문에 피해자 데이터 포함 | 권한 실패 시 본문 없이 응답, 리다이렉트 전에 처리 중단 |
| `ac8.py` | User ID controlled by request parameter with password disclosure | 관리자 계정 페이지의 비밀번호 입력란에 현재 비밀번호가 값으로 채워져 노출 | 비밀번호를 응답에 절대 포함하지 않음, 소유권 검사 |
| `ac10.py` | URL-based access control can be circumvented | 프런트에서 `/admin`을 막지만 백엔드가 `X-Original-Url` 헤더를 신뢰 | 외부에서 들어온 URL 재작성 헤더 제거, 백엔드에서도 권한 검사 |
| `ac11.py` | Method-based access control can be circumvented | POST에만 권한 검사가 있어 GET으로 같은 작업 수행 | 메서드와 무관하게 동일한 권한 검사, 허용 메서드 제한 |
| `ac12.py` | Multi-step process with no access control on one step | 권한 변경의 확인(confirm) 단계에 권한 검사가 없어 바로 호출 가능 | 다단계 처리의 모든 단계에서 권한 검사 |
| `ac13.py` | Referer-based access control | `Referer`가 `/admin`이면 관리자 요청으로 간주 | 조작 가능한 헤더로 권한 판단 금지 |

- `re_practice.py`: CSRF 토큰 추출에 쓰는 정규표현식 연습
