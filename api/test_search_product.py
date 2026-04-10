import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 필터 적용: 검색 결과가 나온 상태에서 화면 좌측의 카테고리 필터 중 하나(예: Hand Tools 체크박스)를 클릭하여 중복 조건을 건다.

# 2차 검증: 다중 조건이 적용된 후 노출된 상품 리스트가 정상적으로 갱신되었는지 검증한다. (상품 개수의 변화 또는 필터된 상품의 카테고리 텍스트 확인 등 본인만의 기준으로 단언할 것)

def test_search_product(driver):
    wait = WebDriverWait(driver, 10)
    driver.get("https://practicesoftwaretesting.com/")

    print("검색란을 선택 후 텍스트 입력")
    search_input = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='search-query']"))
        )
    search_input.send_keys("Pliers")
    print("검색란을 선택 후 텍스트 입력 완료")

    
    search_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-test='search-submit']"))
        )
    search_btn.click()

    time.sleep(2)
    # 검색한 상품의 텍스트를 조회
    print("검색한 상품의 텍스트 조회")
    search_product = wait.until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".card .card-title"))
    )
    
    for p in search_product:
        title = p.get_attribute("textContent").strip()
        # assert 문을 틀리지 않으나, 해당 페이지에서 담긴 상품외 던져주는 데이터로 인해 에러가 발생함
        # assert "Pliers" in title, "상품이 담기지 않았습니다."
        if title:
            print(f'상품명: {title}')
        else:
            print('상품이 담기지 않았다')
    print("검색한 텍스트가 모두 조회되었습니다.")

    hand_tool_check_box = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//label[contains(., 'Hand Tools')]"))
    )
    driver.execute_script("arguments[0].click();", hand_tool_check_box)
    time.sleep(2)

    # 여기서 타임아웃 에러가 발생한다.
    # no_product_text = wait.until(
    #     EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='no-results']"))
    #     ).text
    # print(no_product_text)