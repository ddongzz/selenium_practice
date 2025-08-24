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
        return text in self.driver.title 