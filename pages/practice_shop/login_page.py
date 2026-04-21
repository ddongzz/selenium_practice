# 파일위치 : pages/practice_shop/login_page.py

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class PracticeLoginPage(BasePage):
    URL = "https://practicesoftwaretesting.com/auth/login"

    EMAIL_INPUT = (By.CSS_SELECTOR, "[data-test='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "[data-test='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-test='login-submit']")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='login-error']")

    def __init__(self, driver):
        super().__init__(driver)

    def load(self):
        self.driver.get(self.URL)

    def login(self, email, password):
        self.enter_text(self.EMAIL_INPUT, email)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)
