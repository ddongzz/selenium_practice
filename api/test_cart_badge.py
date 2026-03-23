import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

def test_cart_badge(driver):
    # 1. 페이지 접속 후 로그인
    driver.get("https://www.saucedemo.com/")
    LoginPage(driver).login('standard_user', 'secret_sauce')

    inventory_page = InventoryPage(driver)
    cart_page = CartPage(driver)

    inventory_item_pre = inventory_page.get_first_item_name()
    inventory_page.click_backpack_add_item()

    assert inventory_page.get_cart_badge_text() == "1", "장바구니 벳지 숫자 오류"

    inventory_page.go_to_cart()

    inventory_item_aft = inventory_page.get_first_item_name()
    assert inventory_item_pre == inventory_item_aft, "장바구니에 상품이 정상 등록되지 않았습니다."