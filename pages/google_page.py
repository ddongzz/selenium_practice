from selenium.webdriver.common.by import By

class GooglePage:
    URL = "https://www.google.com"

    def __init__(self, driver):
        self.driver = driver

    # 원하는 요소를 정의
    @property
    def search_box(self):
        return self.driver.find_element(By.NAME, "q")
    
    # 페이지 동작 정의
    def open(self):
        self.driver.get(self.URL)

    def search(self, text):
        self.search_box.send_keys(text)
        self.search_box.submit()

    def title_contains(self, text):
        """
        페이지 타이틀에 text가 포함되어 있는지 확인.
        예시로 "자동화테스트" vs "자동화 테스트" 검색이 동일하도록
        """
        page_title = self.driver.title.replace(" ", "")
        check_text = text.replace(" ", "")
        return check_text in page_title