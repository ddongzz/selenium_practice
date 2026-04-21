# 파일 위치 : pages/practice_shop/home_page.py

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class PracticeHomePage(BasePage):
    URL = "https://practicesoftwaretesting.com/"

    SEARCH_INPUT = (By.CSS_SELECTOR, "[data-test='search-query']")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "[data-test='search-submit']")
    PRODUCT_LIST = (By.CSS_SELECTOR, ".card")
    N0_RESULTS_MESSAGE = (By.CSS_SELECTOR, "[data-test='no-results']")
    PRODUCT_CARD_TITLE = (By.CSS_SELECTOR, ".card-title")

    def __init__(self, driver):
        super().__init__(driver)

    def load(self):
        self.driver.get(self.URL)

    def search_for_item(self, keyword):
        self.enter_text(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)

    def select_hand_tools_category(self):
        self.click(self.CATEGORY_HAND_TOOLS)

    def toggle_category(self, category_name):
        dynamic_locator = (By.XPATH, f"//label[contains(text(), '{category_name}')]/input")
        self.click(dynamic_locator)

    def get_no_results_message(self):
        return self.get_text(self.N0_RESULTS_MESSAGE)
    
    def get_first_product_name(self):
        return self.get_text(self.PRODUCT_CARD_TITLE)
    
    def click_first_product(self):
        self.click(self.PRODUCT_LIST)