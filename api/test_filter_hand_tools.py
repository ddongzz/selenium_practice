import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.parametrize("category_name", [
    "Hammer", "Hand Saw", "Wrench", "Screwdriver", "Pliers", "Chisels", "Measures", "Hand Tools",
    "Grinder", "Sander", "Saw", "Drill", "Power Tools",
    "Tool Belts", "Storage Solutions", "Workbench", "Safety Gear", "Fasteners", "Other",
    "ForgeFlex Tools", "MightyCraft Hardware", "Show only eco-friendly products"
    ])
def test_filter_category(driver, category_name):
    wait = WebDriverWait(driver, 10)

    driver.get("https://practicesoftwaretesting.com/")
    # 해머 체크박스 클릭
    print(f"{category_name} 체크박스를 클릭합니다.")
    hammer_checkbox = wait.until(
        EC.element_to_be_clickable((By.XPATH, f"//label[contains(., '{category_name}')]"))
    )
    hammer_checkbox.click()
    print(f"{category_name} 체크박스 클릭 성공")
    time.sleep(2)
    try:
        product_name = wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".card .card-title"))
        )
        
        for product in product_name:
            print(product.text)
    except:
        no_result = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='no-results']"))
        )
        print(f"상품이 없습니다 : {no_result.text}")


    # 체크박스 해제
    hammer_checkbox.click()
    print(f"{category_name} 체크박스가 해제되었습니다.")
    time.sleep(2)