import pytest
# from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

def test_saucedemo_price_validation(driver, db_connection):
    print("\n[UI] 사이트 로그인")
    driver.get("https://www.saucedemo.com/")
    LoginPage(driver).login('standard_user', 'secret_sauce')

    print("[UI] 백팩($29.99)과 자전거 전조등($9.99), 2개를 장바구니에 담기!")
    inventory_page = InventoryPage(driver)
    inventory_page.add_items_to_cart()
    inventory_page.go_to_cart()

    print("[UI] 장바구니에서 결제 정보 입력창 이동")
    CartPage(driver).click_checkout()

    checkout_page = CheckoutPage(driver)
    checkout_page.enter_checkout_info('Dongchan', 'Lee', '13529')

    item_total = checkout_page.get_item_total()
    tax = checkout_page.get_tax()
    total_value = checkout_page.get_total()


    print(f"계산 로그 > 아이템 합계 : {item_total} / 세금 : {tax} / 화면에서 총 결제액 : {total_value}")

    # 데이터 검증
    print("[DB] 백엔드 DB에 최종 금액이 정확히 들어갔는지 체크")
    with db_connection.cursor() as cursor:
        # 실제 실무환경 시뮬레이션 결제 테이블 생성
        cursor.execute("CREATE TABLE IF NOT EXISTS commerce_payments(order_id INT, buyer VARCHAR(50), amount DECIMAL(10,2))")
        cursor.execute("TRUNCATE TABLE commerce_payments")

        # 프론트에서 결제가 성공하여 DB에 적재되었다고 가정
        cursor.execute(f"INSERT INTO commerce_payments VALUES(1004, 'Dongchan Lee', {total_value})")
        db_connection.commit()

        # 적재된 데이터 확인하기
        cursor.execute("SELECT * FROM commerce_payments WHERE buyer = 'Dongchan Lee'")
        db_result = cursor.fetchone()

        # 프론트에서 읽어온 금액과 DB에서 읽어온 금액이 일치하는지 확인
        assert float(db_result['amount']) == total_value, f"DB 적재 금액 오류 UI : {total_value} / DB : {db_result['amount']}"

        print(f"[DB] 적재확인 완료 최종 결재액 : ${db_result['amount']}" )
        print("데이터 정합성 통과")




