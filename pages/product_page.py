from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class ProductPage:
    def __init__(self, driver):
        self.driver = driver
        # 요소들의 주소 만들기
        self.SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
        self.ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
        self.ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")

    def select_sort_option(self, option_text):
        # 드롭박스에서 특정 텍스트를 찾아 선택한다.
        # 요소를 매번 새로 찾아서 Stale Element 에러를 방지한다.
        dropdown_element = self.driver.find_element(*self.SORT_DROPDOWN)
        Select(dropdown_element).select_by_visible_text(option_text)

    def get_all_prices(self):
        # 화면에 있는 모든 상품의 가격을 실수 리스트로 뽑아온다
        price_elements = self.driver.find_elements(*self.ITEM_PRICES)
        return [float(price.text.replace('$', '')) for price in price_elements]
    
    def get_all_names(self):
        # 화면에 있는 모든 상품의 문자열 리스트로 뽑아온다.
        name_elements = self.driver.find_elements(*self.ITEM_NAMES)
        return [name.text for name in name_elements]