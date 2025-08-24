from pages.google_page import GooglePage
# assert를 사용하는 이유는 구문 간결 및 에러 내용 및 CI/CD에 필요하다.

def test_google_selenium(driver):
    google = GooglePage(driver)
    google.open()
    google.search("Selenium")
    assert google.title_contains("Selenium") 

def test_google_search_pytyon(driver):
    google = GooglePage(driver)
    google.open()
    google.search("Pytyon pytest")
    assert google.title_contains("Python") or google.title_contains("pytest")