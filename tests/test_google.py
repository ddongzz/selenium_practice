# assert를 사용하는 이유는 구문 간결 및 에러 내용 및 CI/CD에 필요하다.
from pages.google_page import GooglePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_google_selenium(driver):
    google = GooglePage(driver)
    google.open()
    google.search("Selenium")
    # 페이지가 완전히 로드될 때까지 기다리기 위해
    WebDriverWait(driver, 10).until(EC.url_contains("Selenium"))
    assert google.title_contains("Selenium")

def test_google_search_pytyon(driver):
    google = GooglePage(driver)
    google.open()
    google.search("Pytyon pytest")
    assert google.title_contains("Python") or google.title_contains("pytest")