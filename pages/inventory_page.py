from selenium.webdriver.common.by import By

class InventoryPage:
    BACKPACK_ADD_BTN = (By.ID, "add-to-cart-sauce-labs-backpack")
    BIKE_LIGHT_ADD_BTN = (By.ID, "add-to-cart-sauce-labs-bike-light")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    FIRST_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver):
        self.driver = driver

    def add_items_to_cart(self):
        self.driver.find_element(*self.BACKPACK_ADD_BTN).click()
        self.driver.find_element(*self.BIKE_LIGHT_ADD_BTN).click()

    def go_to_cart(self):
        self.driver.find_element(*self.CART_LINK).click()

    def click_backpack_add_item(self):
        self.driver.find_element(*self.BACKPACK_ADD_BTN).click()

    def get_first_item_name(self):
        return self.driver.find_element(*self.FIRST_ITEM_NAME).text
    
    def get_cart_badge_text(self):
        return self.driver.find_element(*self.CART_BADGE).text