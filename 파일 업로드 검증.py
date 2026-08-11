from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

try:
    driver.get("https://filebin.net")
    #driver.maximize_window()

    before_url = driver.current_url

    file_path = os.path.abspath("test.txt")
    file_name = os.path.basename(file_path)

    if not os.path.exists(file_path):
        raise Exception(f"파일이 존재하지 않습니다!: {file_path}")

    upload_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
    )

    upload_input.send_keys(file_path)
    print("📁 파일 업로드 입력 완료")

    wait.until(lambda d: d.current_url != before_url)
    uploaded_url = driver.current_url
    print("✅ 업로드 완료 URL:", uploaded_url)

    time.sleep(2)

    # 파일 링크 찾기
    file_link = wait.until(
        EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), '{file_name}')]"))
    )

    file_href = file_link.get_attribute("href")
    print("✅ 파일 링크:", file_href)

    # raw 링크로 이동 (텍스트 내용 직접 확인 가능)
    raw_url = file_href.replace("/download/", "/raw/")
    driver.get(raw_url)

    time.sleep(2)

    body_text = driver.find_element(By.TAG_NAME, "body").text

    print("\n\n===============================")
    print("📌 업로드된 TXT 파일 내용 출력")
    print("===============================")
    print(body_text)
    print("===============================\n")

    time.sleep(3)

except Exception as e:
    print("❌ 테스트 실패:", e)

finally:
    driver.quit()