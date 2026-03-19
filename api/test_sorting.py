import pytest
from pages.login_page import LoginPage
from pages.product_page import ProductPage

def test_drop_box_sort(driver):
    # 1. 페이지 접속 후 로그인
    driver.get("https://www.saucedemo.com/")
    LoginPage(driver).login('standard_user', 'secret_sauce')
    
    # 상품목록 페이지 객체 생성
    product_page = ProductPage(driver)

    # low to high
    product_page.select_sort_option("Price (low to high)")
    prices = product_page.get_all_prices()
    assert prices == sorted(prices), "Price (low to high) 정렬 실패"

    # high to low
    product_page.select_sort_option("Price (high to low)")
    prices = product_page.get_all_prices()
    assert prices == sorted(prices, reverse=True), "Price (high to low) 정렬 실패"

    # name a to z
    product_page.select_sort_option("Name (A to Z)")
    names = product_page.get_all_names()
    assert names == sorted(names), ("Name (a to z) 정렬 실패")

    # name z to a
    product_page.select_sort_option("Name (Z to A)")
    names = product_page.get_all_names()
    assert names == sorted(names, reverse=True), ("Name (z to a) 정렬 실패")

    print("POM 구조로 리팩토링된 정렬 테스트 통과")