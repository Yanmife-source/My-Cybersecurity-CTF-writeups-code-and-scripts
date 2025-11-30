from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options 
import time
from bs4 import BeautifulSoup



def main():
    # User Input
    product=input("Enter a product to search for: ")
    # Configure the headless option
    options=Options()
    options.add_argument("--headless=new")

    # To specify the path to chromedriver 
    service=Service(executable_path="/home/oluwayanmife/Downloads/chromedriver-linux64/chromedriver")
    driver=webdriver.Chrome(service=service,options=options)
    
    # To navigate to the website
    driver.get("https://jumia.com.ng")
    time.sleep(2.5)

    # Wait till the search bar is present
    print("Searching...")
    search=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.ID,"fi-q")))
    search.send_keys(product + Keys.ENTER)

    # TO wait for the page to load
    time.sleep(4)
    # Parses he page for products name and price
    print("Parsing...")
    soup(driver)
    
    # Exit the webiste and close the browser
    driver.quit()

def soup(driver):
    page=driver.page_source
    obe=BeautifulSoup(page,'html.parser')
    info=obe.find_all('div',class_="info",limit=20)
    for  data in info:
        name=data.find('h3',class_='name').text.strip()
        price=data.find('div',class_='prc').text.strip()
        print( f"Product name: {name}   Price: {price}\n")


if __name__=="__main__":
    main()