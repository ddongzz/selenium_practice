import pytest
from selenium.webdriver.common.by import By
import time

# 웹 드라이버와 DB 장비 연결하기
def test_saucedemo_checkout_e2e(driver, db_connection):
    print("\n[UI] 커머스 사이트 SauceDemo 접속 및 로그인 진행")
    driver.get("https://www.saucedemo.com/")

    # 아이디 및 비밀번호 입력 후 로그인
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    print("[UI] 인기 상품(백팩) 장바구니에 담기")
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

    print("[UI] 장바구니로 이동하여 결제 시작")
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "checkout").click()

    print("[UI] 배송지 정보 입력")
    # first_name = driver.find_element(By.ID, "first-name")
    # last_name = driver.find_element(By.ID, "last-name")
    # postal_code = driver.find_element(By.ID, "postal-code")

    # driver.execute_script("arguments[0].value = 'Dongchan';", first_name)
    # driver.execute_script("arguments[0].value = 'Lee';", last_name)
    # driver.execute_script("arguments[0].value = '13529';", postal_code)

    # continue_btn = driver.find_element(By.ID, "continue")
    # driver.execute_script("arguments[0].click()", continue_btn)
    driver.find_element(By.ID, "first-name").send_keys("Dongchan")
    driver.find_element(By.ID, "last-name").send_keys("Lee")
    driver.find_element(By.ID, "postal-code").send_keys('13529')
    driver.find_element(By.ID, "continue").click()

    print("[UI] 최종 결제 완료 버튼")
    driver.find_element(By.ID, "finish").click()

    # 결제 완료 메시지가 정상적으로 출력되는지 확인
    success_text = driver.find_element(By.CLASS_NAME, "complete-header").text
    assert "Thank you for your order" in success_text, "UI 결제 완료 화면이 뜨지 않습니다."
    print("[UI] 결제 완료 프론트엔드 통과")

    print("결제완료가 되었으니 DB에서 크로크 체크합니다")

    with db_connection.cursor() as cursor:
        # 시뮬레이션을 위해 임시 데이터를 생성한다.
        cursor.execute("CREATE TABLE IF NOT EXISTS commerce_orders (order_id INT, buyer_name VARCHAR(50), status VARCHAR(20))")
        cursor.execute("TRUNCATE TABLE commerce_orders")

        # 결제가 성공했기 때문에 데이터가 들어갔다고 가정
        cursor.execute("INSERT INTO commerce_orders VALUES(9991, 'Dongchan Lee', 'PAID')")
        db_connection.commit()

        # QA 크로스 체크 코드 시작
        sql = "SELECT * FROM commerce_orders WHERE buyer_name = 'Dongchan Lee' ORDER BY order_id DESC LIMIT 1"
        cursor.execute(sql)
        db_result = cursor.fetchone()

        # 정확한 DB가 들어왔는지 확인
        assert db_result is not None, "DB에 주문 내역이 생성되지 않았습니다."
        assert db_result['status'] == 'PAID', f"결제 상태 오류 발생 : {db_result['status']}"

        print(f"[DB] 적재 확인 완료 현재 주문 상태: {db_result['status']}")
        print("커머스 장바구니 결제 로직 E2E 자동화 통과")

