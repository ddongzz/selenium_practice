from selenium.webdriver.common.by import By

class CheckoutPage:
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BTN = (By.ID, "continue")

    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BTN = (By.ID, "finish")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver):
        self.driver = driver

    def enter_checkout_info(self, first, last, postal):
        self.driver.find_element(*self.FIRST_NAME).send_keys(first)
        self.driver.find_element(*self.LAST_NAME).send_keys(last)
        self.driver.find_element(*self.POSTAL_CODE).send_keys(postal)
        self.driver.find_element(*self.CONTINUE_BTN).click()

    def get_item_total(self):
        elements = self.driver.find_elements(*self.ITEM_PRICES)
        return sum([float(el.text.replace("$", "")) for el in elements])
    
    def get_tax(self):
        return float(self.driver.find_element(*self.TAX_LABEL).text.replace("Tax: $", ""))
    
    def get_total(self):
        return float(self.driver.find_element(*self.TOTAL_LABEL).text.replace("Total: $", ""))
    
    def finish_click(self):
        self.driver.find_element(*self.FINISH_BTN).click()
        

    def checkout_complete_comfirm(self):
        return self.driver.find_element(*self.COMPLETE_HEADER).text
        