# assert를 사용하는 이유는 구문 간결 및 에러 내용 및 CI/CD에 필요하다.
from selenium.webdriver.chrome.webdriver import WebDriver
from pages.google_page import GooglePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_google_selenium(driver: WebDriver):
    google = GooglePage(driver)
    google.open()
    google.search("Selenium")
    # 페이지가 완전히 로드될 때까지 기다리기 위해
    WebDriverWait(driver, 10).until(EC.url_contains("Selenium"))
    assert google.title_contains("Selenium")

def test_google_search_pytyon(driver: WebDriver):
    google = GooglePage(driver)
    google.open()
    google.search("Pytyon pytest")
    assert google.title_contains("Python") or google.title_contains("pytest")

# f"실패: 현재 title은 '{driver.title}' 입니다."
def test_google_search_autotesting(driver: WebDriver):
    google = GooglePage(driver)
    google.open()
    google.search("자동화 테스트")
    assert google.title_contains("자동화") or google.title_contains("테스트")
