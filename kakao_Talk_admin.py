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
    driver.get("https://sandbox-admin.talk.kakao.com/login")
    time.sleep(1)

    page_title = driver.title
    print(f"접속 페이지: {page_title}")

    username_box = driver.find_element(By.XPATH, "//*[@id='email']")
    username_box.send_keys("eddy.km")

    time.sleep(1) # 너무 빨라서 입력되는거 보려고 대기

    password_box = driver.find_element(By.XPATH, "//*[@id='password']")
    password_box.send_keys("rktjd7488!!")
    password_box.send_keys(Keys.RETURN)
    
    time.sleep(1)
    
    clickable = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[1]/div[1]/span/span/a")) #로그아웃 버튼 선택
    ).click()

    # clickable = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/div[1]/span/span/a")
    # clickable.click()  

    time.sleep(1) 

finally:
    driver.quit()