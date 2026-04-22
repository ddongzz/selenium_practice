# 파일 위치 : test_cart.py

from pages.practice_shop.home_page import PracticeHomePage
from pages.practice_shop.product_detail_page import ProductDetailPage
import pytest
import time

pytestmark = pytest.mark.ui

def test_add_to_cart_flow(driver):
    print("POM 리팩토링 후 장바구니 담기 시나리오 시작")

    home_page = PracticeHomePage(driver)
    detail_page = ProductDetailPage(driver)

    home_page.load()

    expected_product_name = home_page.get_first_product_name()
    home_page.click_first_product()


    actual_product_name = detail_page.get_detail_product_name()
    assert expected_product_name == actual_product_name, f"{expected_product_name}, {actual_product_name}"
    print(f"상품진입 확인 {actual_product_name}")

    detail_page.add_to_cart()

    detail_page.go_to_cart()
    print("장바구니 페이지로 이동 완료")