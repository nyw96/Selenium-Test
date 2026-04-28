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
    driver.get("샌박 어드민 페이지")
    time.sleep(2)

    page_title = driver.title
    print(f"접속 페이지: {page_title}")

    username_box = driver.find_element(By.XPATH, "//*[@id='username']")
    username_box.send_keys("noah.jh")

    password_box = driver.find_element(By.NAME, "password")
    password_box.send_keys("비밀번호")
    password_box.send_keys(Keys.RETURN)
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='side-bar']/div[1]/div/ul/div[1]/div/ul/li/a"))
    )

    clickable = driver.find_element(By.XPATH, "//*[@id='side-bar']/div[1]/div/ul/div[1]/div/ul/li/a")
    clickable.click()  # ActionChains 대신 간단히 click() 사용 가능

    time.sleep(2) 

finally:
    driver.quit()