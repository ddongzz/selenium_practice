from selenium.webdriver.common.by import By

class CartPage:
    CHECKOUT_BTN = (By.ID, "checkout")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")

    def __init__(self, driver):
        self.driver = driver

    def click_checkout(self):
        self.driver.find_element(*self.CHECKOUT_BTN).click()

    def get_first_item_name(self):
        return self.driver.find_element(*self.ITEM_NAME)