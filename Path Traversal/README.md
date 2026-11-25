# Path Traversal

| 파일 | 랩 | 취약점 | 방어 |
|------|----|--------|------|
| `pathtraversal1.py` | File path traversal, simple case | `filename` 파라미터에 `../../../etc/passwd`를 넣어 웹 루트 밖 파일 읽기 | 파일명을 화이트리스트/ID로 매핑, 정규화한 경로가 기준 디렉터리 안인지 확인 |
| `pathtraversal2.py` | Traversal sequences blocked with absolute path bypass | `../`만 막고 절대경로(`/etc/passwd`)는 허용 | 절대경로 거부, 정규화 후 기준 디렉터리 검증 |
| `pathtraversal3.py`, `pathtraversal3_SecLists.py` | Traversal sequences stripped non-recursively | `../`를 한 번만 제거하므로 `....//`가 제거 후 `../`로 복원 | 문자열 치환 필터 대신 경로 정규화(`realpath`) 후 검증 |
| `pathtraversal4_SecLists.py` | Traversal sequences stripped with superfluous URL-decode | 필터 이후 한 번 더 URL 디코딩되어 이중 인코딩(`%252e%252e%252f`)으로 우회 | 디코딩은 한 번만, 디코딩이 끝난 최종 값으로 검증 |
| `pathtraversal5_SecLists.py` | Validation of start of path | 경로가 `/var/www/images/`로 시작하는지만 확인해 `/var/www/images/../../../etc/passwd` 허용 | 정규화한 뒤 시작 경로 검증 |
| `pathtraversal6_SecLists copy.py` | Validation of file extension with null byte bypass | `.jpg`로 끝나는지만 확인해 `%00.jpg`로 확장자 검사 통과 | 널바이트 거부, 정규화 후 확장자와 경로 검증 |

- `lfi_jhaddix.txt`: [SecLists](https://github.com/danielmiessler/SecLists)의 `Fuzzing/LFI/LFI-Jhaddix.txt` (MIT 라이선스). `*_SecLists.py` 스크립트가 이 목록으로 퍼징합니다.
- `source_for_lif_jhaddix.md`: 위 워드리스트를 내려받은 명령
