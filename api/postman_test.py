import pytest
import requests
import pymysql

#실무에서 환경 변수(Environment)처럼 쓰는 기본 주소
BASE_URL = "https://dummyjson.com"

def test_login_success():
    """ TC-01: 정상 로그인 시 200 OK와 토큰을 발급받는지 확인한다.(로그인 통과)"""

    # 1. 세팅(포스트맨 주소창과 Body 입력)
    url = f"{BASE_URL}/auth/login"
    payload = {
        "username" : "emilys",
        "password" : "emilyspass"
    }

    # 2. 전송 (포스트맨의 Send 버튼 클릭)
    response = (requests.post(url, json=payload))

    # 3. QA의 눈으로 결과 확인(자동화의 핵심 : assert(에러가 발생하는지 아닌지 확인하는것))
    # "상태코드가 200이 아니면 여기서 에러를 내고 멈춰라"
    assert response.status_code == 200

    # 응답 데이터를  JSON 형대로 변환
    data = response.json()

    # 응답 데이터 안에 'accessToken'이라는 글자가 무조건 있는지 확인
    assert "accessToken" in data

    # 터미널에 결과 
    print(f"\n[자동화테스트 통과] 토큰 발급 완료 : {data['accessToken'][:15]}...")

def test_login_fail_wrong_password():
    """TC-02: 비밀번호가 틀렸을 때 400 에러와 안내 메시지가 오는지 확인한다.(비밀번호 에러 방어 통과)"""

    url = f"{BASE_URL}/auth/login"
    payload = {
       "username" : "emilys",
       "password" : "wrongpassword"
        }

    # 전송
    response = requests.post(url, json=payload)

    # 2. 상태 코드가 400인 경우
    assert response.status_code == 400

    # 3. 에러 메시지 디테일 확인
    data = response.json()
    assert data["message"] == "Invalid credentials"

    print("\n[자동화 테스트 통과] 예외 처리 방어 성공 400 에러 발생")    

def test_get_my_info_with_token():
    """TC-03: 발금받은 토큰(카드키)으로 내 정보를 성공적으로 조회한다.(토큰 연동해서 내 정보 조회 통과)"""

    # 1. 프런트데스트(로그인)에서 토큰 발급받기
    login_url = f"{BASE_URL}/auth/login"
    login_payload = {"username" : "emilys", "password" : "emilyspass"}
    login_response = requests.post(login_url, json=login_payload)

    #포스트맨의 환경변수 저장과 같은 역할(Token)
    token = login_response.json()["accessToken"]

    # 2. 내 정보 API로 이동
    me_url = f"{BASE_URL}/auth/me"

    # 3. 포스트맨의 Authorization 탭 세팅과 같은 역할
    headers = {
        "Authorization" : f"Bearer {token}"
    }

    # 4. 카드키(header) 들고 Get 요청
    me_response = requests.get(me_url, headers=headers)

    # 5 결과를 눈으로 확인하는 것
    assert me_response.status_code == 200
    assert me_response.json()["username"] == "emilys"

    print("\n[자동화테스트 통과] 카드키(토큰) 인증 성공 에밀리 정보 확인")

# 아래 배열에 있는 데이터 개수 만큼 이 테스트를 반복 실행해라
@pytest.mark.parametrize("test_id, req_username, req_password, expected_status", [
                         ("TC-04: 비밀번호 틀림", "emilys", "wrongpass", 400),
                         ("TC-05: 존재하지 않는 유저", "ghost_user", "emilyspass", 400),
                         ("TC-06: 비밀번호 빈칸", "emilys", "", 400)
])

def test_login_multiple_failures(test_id, req_username, req_password, expected_status):
    """여러 가지 로그인 실패 상황(Edge Case)을 하나의 코드로 검증한다."""

    url = f"{BASE_URL}/auth/login"
    payload = {
        "username" : req_username,
        "password" : req_password
    }

    response = requests.post(url, json=payload)

    assert response.status_code == expected_status

    print(f"\n[{test_id}] 통과 여러개의 에러 방어 작동" )

def test_verify_user_in_local_db(db_connection):
    
    # 데이터베이스 연결 
    with db_connection.cursor() as cursor:
        sql = "SELECT * FROM users WHERE email = 'test@example.com'"
        cursor.execute(sql)

        result = cursor.fetchone()
        
        # 검증에 대한 내용
        assert result is not None, "데이터베이스를 못찾았어요"
        assert result['status'] == 'ACTIVE'

        print("\n 코드 다이어트 성공")

   
