# API Testing

| 파일 | 랩 | 취약점 | 방어 |
|------|----|--------|------|
| `apitest1.py` | Exploiting an API endpoint using documentation | `/api/` 문서가 공개되어 있고, 문서에 나온 `DELETE /api/user/{username}`에 권한 검사가 없음 | 내부 API 문서 비공개, 엔드포인트별 권한 검사 |
| `apitest3.py` | Finding and exploiting an unused API endpoint | `OPTIONS`로 숨은 `PATCH` 메서드를 찾아 상품 가격을 0으로 변경 | 사용하지 않는 메서드 비활성화, 가격 변경에 관리자 권한 요구 |
| `apitest4.py` | Exploiting a mass assignment vulnerability | GET 응답에만 보이던 `chosen_discount` 필드를 POST에 넣으면 그대로 반영되어 100% 할인 | 요청에서 받을 필드를 화이트리스트로 바인딩 |
