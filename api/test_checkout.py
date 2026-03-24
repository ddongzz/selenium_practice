import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

def test_checkout(driver):
    # 1. 페이지 접속 후 로그인
    driver.get("https://www.saucedemo.com/")
    LoginPage(driver).login('standard_user', 'secret_sauce')

    inventory_page = InventoryPage(driver)
    inventory_page.add_items_to_cart()
    inventory_page.go_to_cart()

    cart_page = CartPage(driver)
    cart_page.click_checkout()

    checkout_page = CheckoutPage(driver)
    checkout_page.enter_checkout_info('Dongchan', 'Lee', '13529')
    
    checkout_page.get_item_total()
    checkout_page.get_total()

    checkout_page.finish_click()

    complete_text = checkout_page.checkout_complete_comfirm()
    # 실패 이미지 저장을 위해 잠시 값 수정, 기존 값 : Thank you for your order!
    assert complete_text == "Thank  for your order!", "주문이 완료되지 않았습니다."



    

