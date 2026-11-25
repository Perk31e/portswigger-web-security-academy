# Cross-Site Scripting (XSS)

| 파일 | 랩 | 취약점 | 방어 |
|------|----|--------|------|
| `xss1.py` | Reflected XSS into HTML context with nothing encoded | 검색어가 인코딩 없이 HTML에 반사되어 `<script>alert(1)</script>` 실행 | 출력 위치에 맞는 HTML 인코딩, CSP |
| `xss2.py` | Stored XSS into HTML context with nothing encoded | 댓글이 인코딩 없이 저장된 뒤 출력 | 저장된 데이터도 출력 시 인코딩 |
| `xss3.py` | DOM XSS in `document.write` sink using source `location.search` | URL 값을 `document.write`로 그대로 써서 `"><svg onload=alert(1)>`로 속성 탈출 | 위험한 sink 대신 `textContent` 등 안전한 API 사용 |
| `xss4.py` | DOM XSS in `innerHTML` sink using source `location.search` | `innerHTML`은 `<script>`를 실행하지 않으므로 `<img onerror>`로 실행 | `innerHTML` 대신 `textContent`, 필요하면 DOMPurify |
| `xss5.py` | DOM XSS in jQuery anchor `href` attribute sink using `location.search` source | `returnPath`가 링크 `href`로 들어가 `javascript:alert(1)` 실행 | URL 스킴을 `http(s)`로 제한 |
| `xss8.py` | Stored XSS into anchor `href` attribute with double quotes HTML-encoded | 댓글의 웹사이트 값이 `href`에 들어가며, 따옴표만 인코딩하고 `javascript:` 스킴은 허용 | 스킴 화이트리스트, 속성 컨텍스트 인코딩 |
| `xss9.py` | Reflected XSS into a JavaScript string with angle brackets HTML encoded | `<>`만 인코딩되고 JS 문자열 안에 반사되어 `';alert(1);'`로 문자열 탈출 | JS 컨텍스트용 인코딩, 데이터는 JSON으로 전달 |
| `xss18.py` | Reflected XSS into a JavaScript string with single quote and backslash escaped | `'`와 `\`는 이스케이프되지만 `</script>`로 스크립트 블록 자체를 닫고 새 태그 삽입 | JS 컨텍스트에서 `<`, `/`까지 인코딩, CSP |
