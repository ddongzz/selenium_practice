# 파일 위치 : api/test_filter_hand_tools.py

import pytest
import time
from pages.practice_shop.home_page import PracticeHomePage

pytestmart = pytest.mark.ui

def test_filter_hand_tools(driver):
    print("POM 리팩토링 후 테스트 시작")
    
    home_page = PracticeHomePage(driver)

    home_page.load()

    target_categories = [
        "Hammer", "Hand Saw", "Wrench", "Screwdriver", "Pliers", "Chisels", "Measures", "Hand Tools",
        "Grinder", "Sander", "Saw", "Drill", "Power Tools",
        "Tool Belts", "Storage Solutions", "Workbench", "Safety Gear", "Fasteners", "Other",
        "ForgeFlex Tools", "MightyCraft Hardware", "Show only eco-friendly products"
    ]
    for category in target_categories:
        print(f"{category} 필터 테스트 시작")

        # 선택
        home_page.toggle_category(category)
        time.sleep(2)

        # 확인
        product_list = home_page.driver.find_elements(*home_page.PRODUCT_LIST)
        if len(product_list) > 0:
            print(f"검색된 상품 수 : {len(product_list)}")
        else:
            no_result_msg = home_page.get_no_results_message()
            assert no_result_msg == "There are no products found.", "안내문구가 없습니다."
            print(f"{no_result_msg}가 출력되었습니다.")

        # 해제
        home_page.toggle_category(category)
        time.sleep(2)

    print("필터 테스트가 완료되었습니다.")




