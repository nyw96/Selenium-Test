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
    driver.get("https://www.naver.com")

    wait = WebDriverWait(driver, 10)

    # 1. 검색창 찾기
    search_box = wait.until(
        EC.element_to_be_clickable((By.NAME, "query"))
    )

    # 2. 검색어 입력
    search_box.click()
    search_box.send_keys("카카오T1")

    # 3. 검색 실행 (엔터)
    search_box.send_keys(Keys.ENTER)

    # 또는 버튼 클릭 방식도 가능
    # search_btn = wait.until(
    #     EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_search"))
    # )
    # search_btn.click()

    # 4. 결과 확인 (예: 결과 페이지 타이틀)
    wait.until(EC.title_contains("카카오T"))
    #print("검색 성공:", driver.title)

finally:
    time.sleep(10)
    driver.quit()