import os
import pytest
import pymysql
import allure
import uuid
import requests
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
    options.add_argument("--disable-gpu") # GPU 가속 끄기
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # 비밀번호 경고창 안뜨게 하기 위해
    options.add_argument("--incognito")
    # 창의 사이즈를 고정해서 미출력되거나 클릭되지 않는 상태를 제거하기 위해
    options.add_argument('--window-size=1920,1080')
    options.add_argument("--disable-extensions") # 불필요한 확장 프로그램 차단
    options.add_argument("--blick-settins=imagesEnable=false") # 웹페이지 로딩 차단(중요)
    options.page_load_strategy = 'eager' # 뼈대(DOM)만 그려지면 바로 테스트 시작하다록 하는것 (자잘한 스크립트 대기 X)

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

# --------------------------------------------------------------------------
# 병렬 테스트용 임시 유저 발급 장비 (Data Isolation)
# --------------------------------------------------------------------------

@pytest.fixture
def temp_user(api_context):
    unique_name = f"QA_User_{uuid.uuid4().hex[:6]}"
    payload = {"name": unique_name, "job": "Tester"}

    response = requests.post(api_context["url"], json=payload, headers=api_context["headers"])
    new_user_id = response.json()['id']
    print(f"\n 워커 전용 임시 유저 생성, ID: {new_user_id}")

    # 테스트 함수로 새로 만든 유저의 ID를 넘겨준다.
    yield new_user_id

    # 테스트가 끝나면 사용한 유저만 타겟팅해서 지운다.
    delete_url = f"{api_context['url']}/{new_user_id}"
    requests.delete(delete_url, headers=api_context["headers"])
    print(f"임시 유저 삭제 완료, ID : {new_user_id}")