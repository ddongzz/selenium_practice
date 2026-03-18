import pytest
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def test_drop_box_sort(driver):
    # 1. 페이지 접속 후 로그인
    driver.get("https://www.saucedemo.com/")
    LoginPage(driver).login('standard_user', 'secret_sauce')

    # --- [테스트 1: Price (low to high)] ---
    # 드롭박스를 매번 새로 찾아야 화면이 갱신되어도 에러가 나지 않습니다.
    sort_dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
    sort_dropdown.select_by_visible_text("Price (low to high)")
    
    price_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    # '$' 기호를 떼고 실수(float)로 변환하여 리스트 생성 (리스트 컴프리헨션 사용)
    prices_low_to_high = [float(price.text.replace('$', '')) for price in price_elements]
    assert prices_low_to_high == sorted(prices_low_to_high), " Price (low to high) 정렬 실패!"

    # --- [테스트 2: Price (high to low)] ---
    sort_dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
    sort_dropdown.select_by_visible_text("Price (high to low)")
    
    price_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    prices_high_to_low = [float(price.text.replace('$', '')) for price in price_elements]
    # reverse=True 를 주면 내림차순(큰 수 -> 작은 수) 정렬이 됩니다.
    assert prices_high_to_low == sorted(prices_high_to_low, reverse=True), " Price (high to low) 정렬 실패!"

    # --- [테스트 3: Name (A to Z)] ---
    sort_dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
    sort_dropdown.select_by_visible_text("Name (A to Z)")
    
    name_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    names_a_to_z = [name.text for name in name_elements]
    assert names_a_to_z == sorted(names_a_to_z), " Name (A to Z) 정렬 실패!"

    # --- [테스트 4: Name (Z to A)] ---
    sort_dropdown = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
    sort_dropdown.select_by_visible_text("Name (Z to A)")
    
    name_elements = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    names_z_to_a = [name.text for name in name_elements]
    assert names_z_to_a == sorted(names_z_to_a, reverse=True), " Name (Z to A) 정렬 실패!"

    print("\n 4가지 정렬 조건 모두 완벽하게 통과했습니다!")