# SSRF

| 파일 | 랩 | 취약점 | 방어 |
|------|----|--------|------|
| `ssrf1.py` | Basic SSRF against the local server | 재고 조회 `stockApi`에 `http://localhost/admin`을 넣어 서버가 스스로 관리자 페이지를 요청 | 요청 대상 URL 화이트리스트, 내부 관리 기능에도 인증 |
| `ssrf2.py` | Basic SSRF against another back-end system | `192.168.0.1~255:8080/admin`을 순회해 내부망 관리자 서버를 찾아 접근 | 내부 대역 요청 차단, 서버 아웃바운드 네트워크 분리 |
| `ssrf4.py` | SSRF with blacklist-based input filter | `127.0.0.1`과 `admin` 문자열 차단을 `127.1`과 `%2561dmin`(이중 인코딩)으로 우회 | 블랙리스트 대신 화이트리스트, 호스트를 IP로 해석한 뒤 검증 |
| `ssrf5.py` | SSRF with filter bypass via open redirection vulnerability | 같은 사이트 경로만 허용하지만, 사이트 내 오픈 리다이렉트(`/product/nextProduct?path=`)로 내부 주소에 도달 | 오픈 리다이렉트 제거, 서버 측 요청에서 리다이렉트 따라가지 않기 |
