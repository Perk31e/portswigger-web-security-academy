# CSRF

| 파일 | 랩 | 취약점 | 방어 |
|------|----|--------|------|
| `csrf1.py` | CSRF vulnerability with no defenses | 이메일 변경 요청에 CSRF 토큰이 없어, 공격자 사이트의 자동 제출 폼으로 피해자 이메일 변경 | CSRF 토큰, `SameSite` 쿠키 |
| `csrf2.py` | CSRF where token validation depends on request method | POST만 토큰을 검사하고, GET은 같은 기능을 토큰 없이 처리 | 상태 변경은 POST만 허용, 모든 메서드에서 토큰 검증 |

- 스크립트는 페이로드 HTML을 만들어 Academy의 exploit server에 저장하고 피해자에게 전달(Deliver)하는 과정까지 자동화했습니다. 실제 JS 실행은 랩의 피해자 브라우저가 합니다.
