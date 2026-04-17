from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

SEARCH_KEYWORD = "Kakao"

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    wait = WebDriverWait(driver, 15)

    driver.get("https://en.wikipedia.org/wiki/Main_Page")
    #driver.maximize_window()

    # 검색
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "search")))
    search_box.click()
    search_box.send_keys(SEARCH_KEYWORD)
    search_box.send_keys(Keys.ENTER)

    # 제목 (innerText로 추출)
    heading = wait.until(EC.presence_of_element_located((By.ID, "firstHeading")))
    title_text = driver.execute_script("return arguments[0].innerText;", heading)

    print("✅ 검색 성공")
    print("📌 검색 결과 제목:", title_text)

    # 문단들 찾기
    paragraphs = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.mw-content-container p"))
    )

    first_text_paragraph = None

    for p in paragraphs:
        paragraph_text = driver.execute_script("return arguments[0].innerText;", p).strip()
        if paragraph_text:
            first_text_paragraph = paragraph_text
            break

    if first_text_paragraph:
        print("📌 첫 문단 내용:", first_text_paragraph)
    else:
        print("⚠️ 문단 내용이 비어있습니다.")

    time.sleep(3)

except Exception as e:
    print("❌ 테스트 실패")
    print("에러 내용:", e)

finally:
    driver.quit()