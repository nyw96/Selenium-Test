from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    driver.get("https://www.naver.com")
    driver.maximize_window()

    # 1) 검색
    search_box = wait.until(EC.presence_of_element_located((By.ID, "query")))
    search_box.click()
    search_box.send_keys("디케이테크인")
    search_box.send_keys(Keys.ENTER)

    wait.until(EC.url_contains("search.naver.com"))

    # 2) 뉴스 탭 이동
    news_tab = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "뉴스")))
    news_tab.click()

    wait.until(EC.url_contains("where=news"))
    time.sleep(2)

    print("✅ 뉴스 탭 진입 완료")
    print("현재 URL:", driver.current_url)
 
    # -----------------------------
    # 3) 최신순 클릭 검증
    # -----------------------------
    latest_sort = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'최신순')]"))
    )
    latest_sort.click()

    time.sleep(2)

    latest_url = driver.current_url
    print("\n✅ 최신순 클릭 후 URL:", latest_url)

    assert "sort=1" in latest_url, "❌ 최신순 정렬 실패 (sort=1 없음)"
    print("✅ 최신순 정렬 검증 성공 (sort=1 확인)")

    # -----------------------------
    # 4) 관련도순 클릭 검증
    # -----------------------------
    relevance_sort = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'관련도순')]"))
    )
    relevance_sort.click()

    time.sleep(2)

    relevance_url = driver.current_url
    print("\n✅ 관련도순 클릭 후 URL:", relevance_url)

    assert "sort=0" in relevance_url, "❌ 관련도순 정렬 실패 (sort=0 없음)"
    print("✅ 관련도순 정렬 검증 성공 (sort=0 확인)")

    time.sleep(2)
    
        # 3) 첫번째 기사 선택 (mark 태그에 디케이테크인 포함된 span 찾기)
    target_span = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "(//span[contains(@class,'sds-comps-text')][.//mark[contains(text(),'디케이테크인')]])[1]")
        )
    )

    target_link = target_span.find_element(By.XPATH, "./ancestor::a[1]")

   # old_windows = driver.window_handles[1]
   # original_window = driver.current_window_handle

    target_link.click()
    print("✅ 첫번째 기사 클릭 완료")
    time.sleep(2)
    
    original_window = driver.window_handles[0]  # 또는 저장해둔 original_window
    print("✅ 뉴스 탭 저장 완료")
    time.sleep(2)
    
    driver.switch_to.window(original_window)
    print("✅ 탭 전환 완료1")
    time.sleep(2)

    #driver.close()
    print("✅ 종료 완료")
    time.sleep(3)
    
except AssertionError as ae:
    print(str(ae))

except Exception as e:
    print("❌ 테스트 실패:", e)
    

finally:
    driver.quit()