import requests
from bs4 import BeautifulSoup

session=requests.Session()

def main():
    matric_no=input('Enter your matric no: ')
    password=input('Enter your password: ')


    login_url="https://eportal.oauife.edu.ng/login.php"
    login=requests.get(login_url)


    payload={
        "user_id":matric_no,
        "pswd":password,
        "SessionF":"2024",
        "SemesterF":"0",
        "Submit":"Submit"
    }
    submit_url="https://eportal.oauife.edu.ng/login1.php"
    
    response=session.post(submit_url,data=payload)
    print(response.text[:2000])
    print(response.status_code)

def raw_score():
    result_url="https://eportal.oauife.edu.ng/viewrawscore1.php"
    result_response=session.post(result_url)
    soup=BeautifulSoup(result_response.text,'html-parser')
    table=soup.find_all('table')
    rows=table.find_all('tr')
    for cell in rows:
        course_code=cell.find_all('td')[0].text.strip()
        score=cell.find_all('td')[-1].text.strip()
        print(f'Course: {course_code} Score: {score}')
         
def course_reg():
    ...


if __name__=="__main__":
    main()