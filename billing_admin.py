import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Keys, ActionChains

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    driver.get("https://빌링 어드민 페이지")
    time.sleep(1)

    page_title = driver.title
    print(f"접속 페이지: {page_title}")

    username_box = driver.find_element(By.XPATH, "//*[@id='username']")
    username_box.send_keys("eddy.km@kakaomobility.com")

    time.sleep(1) # 너무 빨라서 입력되는거 보려고

    password_box = driver.find_element(By.XPATH, "//*[@id='password']")
    password_box.send_keys("rktjd7488!!")
    password_box.send_keys(Keys.RETURN)
    
    time.sleep(1)
    
    clickable = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='logout_form']/a")) #로그아웃 버튼 선택
    ).click()

    #clickable = driver.find_element(By.XPATH, "//*[@id='logout_form']/a")
    #clickable.click()  
    
    time.sleep(1) 

finally:
    driver.quit()