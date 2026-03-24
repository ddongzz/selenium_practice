import pytest
import pymysql
import allure
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

    connection.close()

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
                driver.get_screenshoot_as_png(),
                name = "에러 발생 이미지",
                attachment_type=AttachmentType.PNG
            )
