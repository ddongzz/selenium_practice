import os
import pytest
import pymysql
import allure
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from allure_commons.types import AttachmentType

# --------------------------------------------------------------------------
# 웹 브라우저 장비
# --------------------------------------------------------------------------

@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    options = Options()
    options.add_argument("--headless") # GUI가 없는 GitHub Actions 때문에
    # options.add_argument("--disable-gpu") # GPU 가속 끄기
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # 비밀번호 경고창 안뜨게 하기 위해
    options.add_argument("--incognito")
    # 창의 사이즈를 고정해서 미출력되거나 클릭되지 않는 상태를 제거하기 위해
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()

# --------------------------------------------------------------------------
# 데이터베이스 장비
# --------------------------------------------------------------------------

@pytest.fixture(scope="function")
def db_connection():
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='1111',
        db='qa_test',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection.cursor() as cursor:
        # 가짜 데이터 넣기
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT, email VARCHAR(50), status VARCHAR(10))")
        cursor.execute("TRUNCATE TABLE users")
        cursor.execute("INSERT INTO users VALUES(1, 'test@example.com', 'ACTIVE')")
        connection.commit()

    yield connection 
    # 테스트 종료 후 뒤처리 (성공/실패 상관없이 무조건 실행됨)
    try:
        with connection.cursor() as cursor:
            # test_integration.py에서 만든 실무용 테이블 비우기
            cursor.execute("TRUNCATE TABLE real_users")
            connection.commit()
            print("\n [클린업] 테스트 종료 : real_users 테이블 데이터를 완벽하게 초기화했습니다.")
    finally:
        connection.close()
        print("DB 연결을 안전하게 종료했습니다.")
    

# --------------------------------------------------------------------------
# API 테스트 장비 
# --------------------------------------------------------------------------

@pytest.fixture
def api_context():
    base_url = "https://reqres.in/api/users"

    # .env 파일에 있는 API 키를 불러옴
    headers = {
        "x-api-key": os.getenv("REQRES_API_KEY")
    }
    return {"url": base_url, "headers": headers}

# --------------------------------------------------------------------------
# Allure 리포트 훅
# --------------------------------------------------------------------------

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # 테스트가 실패한 경우
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            # Allure 리포트에 스크린샷을 첨부하기 위해
            allure.attach(
                driver.get_screenshot_as_png(),
                name = "에러 발생 이미지",
                attachment_type=AttachmentType.PNG
            )
