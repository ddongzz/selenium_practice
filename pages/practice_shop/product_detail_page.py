# 파일 위치 : pages/practice_shop/product_detail_page.py

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductDetailPage(BasePage):
    PRODUCT_NAME = (By.CSS_SELECTOR, "[data-test='product-name']")
    ADD_TO_CART_BTN = (By.CSS_SELECTOR, "[data-test='add-to-cart']")

    def __init__(self, driver):
        super().__init__(driver)

    def get_detail_product_name(self):
        return self.get_text(self.PRODUCT_NAME)
    
    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BTN)