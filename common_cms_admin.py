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
    driver.get("https://샌박 어드민 페이지")
    time.sleep(1)

    page_title = driver.title
    print(f"접속 페이지: {page_title}")

    username_box = driver.find_element(By.XPATH, "//*[@id='username']")
    username_box.send_keys("eddy.km")
    

    password_box = driver.find_element(By.NAME, "password")
    password_box.send_keys("rktjd7488!!")
    password_box.send_keys(Keys.RETURN)
    
    time.sleep(1) # 페이지 로딩 대기 시간
    
    clickable = driver.find_element(By.XPATH, "//*[@id='root']/div/header/div[2]")
    clickable.click()  #계정 버튼 선택
  
    click_logout = WebDriverWait(driver, 10).until( #계정 버튼 선택 후 로그아웃 버튼이 눈에 보일때까지 최대 10초 대기
    EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/ul/li"))
    ).click() # 하위 로그아웃 버튼 선택
       
    #click_logout.click() 
    time.sleep(1) 

finally:
    driver.quit()