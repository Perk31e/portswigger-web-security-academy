# File Upload Vulnerabilities

| 파일 | 랩 | 취약점 | 방어 |
|------|----|--------|------|
| `upload1.py` | Remote code execution via web shell upload | 아바타 업로드에 검증이 없어 PHP 웹셸 업로드 후 실행 | 확장자·내용 화이트리스트, 업로드 폴더 실행 권한 제거 |
| `upload2.py` | Web shell upload via Content-Type restriction bypass | 클라이언트가 보낸 `Content-Type`만 확인해 `image/jpeg`로 바꾸면 통과 | 헤더가 아닌 실제 파일 내용과 확장자로 검증 |
| `upload3.py` | Web shell upload via path traversal | 업로드 폴더는 실행이 막혀 있지만 파일명 `..%2fweb_shell.php`로 상위 폴더에 저장 | 서버에서 파일명을 새로 생성, 경로 문자 제거 |
| `upload4.py` | Web shell upload via extension blacklist bypass | `.htaccess`를 올려 임의 확장자(`.133t`)를 PHP로 실행하도록 설정 | 블랙리스트 대신 화이트리스트, 설정 파일 업로드 차단 |
| `upload5.py` | Web shell upload via obfuscated file extension | `web_shell.php%00.jpg`에서 검증은 `.jpg`로, 저장은 `.php`로 처리 | 널바이트 거부, 디코딩 후 최종 파일명으로 검증 |
| `upload6.py` | Remote code execution via polyglot web shell upload | PNG 메타데이터(Comment)에 PHP 코드를 넣은 폴리글롯이 이미지 검증을 통과 | 이미지 재인코딩, 업로드 폴더에서 스크립트 실행 금지 |

- `payload.txt`: 웹셸 코드 (`system($_GET['cmd'])`)
- `test.png`, `polyglot.php`: `exiftool "-Comment<=payload.txt" test.png -o polyglot.php`로 만든 폴리글롯의 원본과 결과물
- `web_shell.php`: `upload1~5.py`가 업로드하는 파일. 저장소에는 넣지 않았으니 `payload.txt` 내용으로 직접 만들어 쓰면 됩니다.
