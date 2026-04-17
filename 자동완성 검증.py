from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://www.naver.com")
    driver.maximize_window()

    # 1) 검색창 입력
    search_box = wait.until(EC.presence_of_element_located((By.ID, "query")))
    search_box.click()
    search_box.send_keys("디케이테크인")

    time.sleep(1)  # 자동완성 렌더링 대기

    # 2) 자동완성 추천어 리스트 가져오기 (a.kwd)
    suggestions = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.kwd"))
    )

    print(f"✅ 자동완성 추천어 개수: {len(suggestions)}")

    # 3) 추천어 텍스트 출력
    for i, item in enumerate(suggestions[:5]):
        print(f"{i+1}. {item.text}")

    # 4) 첫번째 추천어 클릭
    first_text = suggestions[0].text
    suggestions[3].click()

    # 5) 검색 결과 페이지 이동 확인
    wait.until(EC.url_contains("search.naver.com"))

    
    # 6) 검색결과 화면에서 "디케이테크인" 문구 보이면 클릭
    target = wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//span[contains(@class,'sds-comps-text')][.//mark[contains(text(),'디케이테크인')]]")
        )
    )
    target.click()

    print("✅ 검색 결과 페이지 이동 성공")
    print("선택한 추천어:", first_text)
    #print("현재 URL:", driver.current_url)

    time.sleep(5)

except Exception as e:
    print("❌ 테스트 실패:", e)

finally:
    
    time.sleep(5)
    driver.quit()