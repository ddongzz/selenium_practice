from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def find_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    def click(self, locator):
        self.find_element(locator).click()

    def enter_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        def _text_is_present(driver):
            try:
                element = driver.find_element(*locator)
                return len(element.text.strip()) > 0
            except (StaleElementReferenceException, NoSuchElementException):
                return False
        
        self.wait.until(_text_is_present)
        return self.driver.find_element(*locator).text
    
    def get_title(self):
        return self.driver.title
    
    NAV_CART_BTN = (By.CSS_SELECTOR, "[data-test='nav-cart']")

    def go_to_cart(self):
        self.click(self.NAV_CART_BTN)