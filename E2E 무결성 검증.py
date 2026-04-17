from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import hashlib
import requests


def normalize_text(text):
    return text.replace("\ufeff", "").replace("\r\n", "\n").strip()


def get_md5(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def read_local_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

try:
    print("🚀 테스트 시작")

    driver.get("https://filebin.net")
    driver.maximize_window()

    before_url = driver.current_url

    file_path = os.path.abspath("test.txt")
    file_name = os.path.basename(file_path)

    if not os.path.exists(file_path):
        raise Exception(f"파일 없음: {file_path}")

    local_text = normalize_text(read_local_file(file_path))
    local_hash = get_md5(local_text)

    print("📌 로컬 MD5:", local_hash)

    upload_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
    )

    upload_input.send_keys(file_path)
    print("📁 업로드 입력 완료")

    wait.until(lambda d: d.current_url != before_url)
    print("✅ 업로드 완료 URL:", driver.current_url)

    time.sleep(2)

    file_link = wait.until(
        EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), '{file_name}')]"))
    )

    file_href = file_link.get_attribute("href")
    print("✅ 다운로드 링크:", file_href)

    # 🔥 raw_url 변환하지 말고, 그냥 다운로드 링크를 requests로 받아서 확인
    response = requests.get(file_href)

    print("status:", response.status_code)
    print("content-type:", response.headers.get("Content-Type"))
    print("응답 앞부분 200자:", response.text[:200])

    if response.status_code != 200:
        raise Exception("❌ 다운로드 실패")

    uploaded_text = normalize_text(response.text)
    uploaded_hash = get_md5(uploaded_text)

    print("📌 업로드 MD5:", uploaded_hash)

    if local_hash == uploaded_hash:
        print("\n🎉 PASS: 업로드 파일 내용 동일")
    else:
        print("\n❌ FAIL: 업로드 파일 내용 불일치")
        print("\n------ 로컬 ------")
        print(local_text)
        print("\n------ 업로드 ------")
        print(uploaded_text)
        raise Exception("❌ 무결성 검증 FAIL (MD5 불일치)")

except Exception as e:
    print("\n===============================")
    print("❌ 테스트 실패")
    print("===============================")
    print(e)
    print("===============================\n")

finally:
    driver.quit()