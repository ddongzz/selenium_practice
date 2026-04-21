# 파일 위치 : test_login.py

import pytest
import time
from pages.practice_shop.login_page import PracticeLoginPage

pytestmark = pytest.mark.ui

def test_valid_login(driver):
    print("POM 기반 로그인 시작")

    login_page = PracticeLoginPage(driver)
    login_page.load()

    login_page.login("customer@practicesoftwaretesting.com", "welcome01")

    time.sleep(2)

    current_url = login_page.driver.current_url
    assert "account" in current_url, f"로그인 실패, 현재 URL : {current_url}"
    print("정상 로그인 성공 및 마이페이지 이동 확인")

def test_invalid_login(driver):
    print("POM 기반 비정상 로그인 테스트 시작")

    login_page = PracticeLoginPage(driver)
    login_page.load()

    login_page.login("customer@practicesoftwaretesting.com", "wrongpassword123")

    time.sleep(2)

    error_msg = login_page.get_error_message()
    assert error_msg != "", "로그인 실패 문구가 노출되지 않았습니다."
    print(f"비정상 로그인 차단 확인 : {error_msg}")