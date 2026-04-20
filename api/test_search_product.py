import pytest
from pages.practice_shop.home_page import PracticeHomePage
import time

pytestmark = pytest.mark.usefixtures # UI 마커 유지

def test_search_product(driver):
    print("POM 리팩토링 버전 상품 검색 테스트 시작")

    home_page = PracticeHomePage(driver)

    home_page.load()

    search_keyword = "pliers"
    home_page.search_for_item(search_keyword)

    time.sleep(2)

    product_list = home_page.driver.find_elements(*home_page.PRODUCT_LIST)
    assert len(product_list) > 0, f"'{search_keyword}' 검색 결과가 없습니다."
    print(f"'{search_keyword}' 검색 성공 > 발견된 상품 수 : {len(product_list)}")