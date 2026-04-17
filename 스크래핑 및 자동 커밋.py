from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import datetime
import subprocess
import json
import os

def run(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode == 0

def scrape_naver_sports():
    options = Options()
    options.add_argument("--headless")  # 브라우저 창 안 띄움
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://news.naver.com/sports/index.naver")
        articles = driver.find_elements(By.CSS_SELECTOR, ".sa_text_title, .cjs_t")

        news_list = []
        for article in articles[:20]:  # 상위 20개
            title = article.text.strip()
            link = article.get_attribute("href") or \
                   article.find_element(By.XPATH, "..").get_attribute("href")
            if title:
                news_list.append({"title": title, "link": link})

        return news_list

    finally:
        driver.quit()

def save_and_commit(news_list):
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # 결과 저장 폴더
    os.makedirs("news", exist_ok=True)
    filename = f"news/{date_str}.json"

    # 기존 데이터 불러오기
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    # 새 데이터 추가
    data.append({
        "collected_at": time_str,
        "articles": news_list
    })

    # 파일 저장
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"수집된 기사: {len(news_list)}개")

    # Git 커밋 & 푸시
    run("git add -A")
    if run(f'git commit -m "news: 스포츠 뉴스 수집 {date_str} {time_str}"'):
        if run("git push origin main"):
            print(f"GitHub 푸시 완료!")
        else:
            print("푸시 실패")
    else:
        print("커밋할 변경사항 없음")

if __name__ == "__main__":
    print("네이버 스포츠 뉴스 수집 시작...")
    news = scrape_naver_sports()
    save_and_commit(news)
    print("완료!")