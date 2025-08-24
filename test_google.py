import pytest 
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
# Process completed with exit code 1 발생으로 인해 추가한 코드
from selenium.webdriver.chrome.options import Options
# import time (8/24 pytest 실습하면서 주석처리)

# 8/23일 진행한 것
'''
# Chrome 드라이버 자동 설치 및 실행
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://www.google.com")
time.sleep(2)

search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("ChatGPT")
search_box.submit()

time.sleep(3)
print("테스트 완료")
driver.quit()
'''

@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless") # GUI 없이 실행하기 위해
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

def test_google_search_selenium(driver):
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Selenium")
    search_box.submit()
    assert "Selenium" in driver.title

def test_google_search_python(driver):
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys("Python pytest")
    search_box.submit()
    assert "Python" in driver.title or "pytest" in driver.title

def test_google_search_homepage(driver):
    driver.get("https://www.google.com")
    assert "Google" in driver.title