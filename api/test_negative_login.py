import pytest
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage

# 구조 ("아이디", "비밀번호", "에러메시지")
@pytest.mark.parametrize("username, password, expected_error_msg", [
    ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out"),
    ("standard_user", "wrong_pw_123", "Username and password do not match any user in this service"),
    ("", "secret_sauce", "Username is required")
])

def test_saucedemo_login_negative(driver, username, password, expected_error_msg):
    print(f"\n[UI] 네거티브 테스트 타켓 : ID : '{username}', PW : '{password}'")

    # 매 테스트마다 찌꺼기가 남지 않게 새 페이지로 접속(초기화)
    driver.get("https://www.saucedemo.com/")

    # 로그인 페이지에서 객체를 꺼내오기
    login_page = LoginPage(driver)

    # 아이디와 비밀번호를 해당 객체의 함수에 전달
    login_page.login(username, password)

    # 에러 메시지 객체에서 꺼내오기
    actual_error_msg = login_page.get_error_message()

    print(f"[UI] 실제 발생한 에러 문구 : {actual_error_msg}")

    # assert를 통해 예상한 문구가 맞는지 확인하기
    assert expected_error_msg in actual_error_msg, f"에러메시지 불일치 : (예상 : {expected_error_msg} / 실제 : {actual_error_msg})"
    print("예외처리 방어 로직 통과")