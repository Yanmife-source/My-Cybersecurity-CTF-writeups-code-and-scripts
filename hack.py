import requests
from bs4 import BeautifulSoup

session=requests.Session()

cookies=requests.get("https://eportal.oauife.edu.ng/login.php")
print(cookies)

payload={
    
}