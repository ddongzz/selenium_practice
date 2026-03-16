import requests

# 셀레니움과 데이터베이스를 같이 사용하기
def test_full_e2e_scenario(driver, db_connection):

    # 웹드라이버 연결하기
    print("\n[UI] 가상의 서비스(JSONPlaceholder)에 접속합니다...")
    driver.get("https://jsonplaceholder.typicode.com/")
    assert "JSONPlaceholder" in driver.title, "웹 사이트 접속 실패"
    print("[UI] 웹사이트 정상 로드 및 타이틀 확인 완료")

    # requests로 백엔드 통신하기
    print("[API] 백엔드 서버에 회원 정보를 요청합니다.")

    # 봇인걸 들키지않기 위해 가짜 신분증 만들기
    # headers = {
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    #     }

    response = requests.get("https://jsonplaceholder.typicode.com/users/2")
    assert response.status_code == 200, "API 통신 실패"

    user_email = response.json()['email']
    print(f"[API] 통ㅇ신 성공! 가져온 이메일: {user_email}")

    # API로 가져온 데이터를 로컬 DB에 저장되는지 확인
    print("[DB] 해당 이메일이 DB에 정상 적재되었는지 검증")
    with db_connection.cursor() as cursor:
        # 실무는 API가 DB에 넣겠지만 테스트니까 API에서 빼온 데이터를 직접 DB에 넣는다.
        sql_insert = "INSERT INTO users(id, email, status) VALUES(2, %s, 'ACTIVE')"
        cursor.execute(sql_insert, (user_email,))
        db_connection.commit()

        # 크로스 체크
        sql_select = "SELECT * FROM users WHERE email = %s"
        cursor.execute(sql_select, (user_email,))
        db_result = cursor.fetchone()

        # 검증
        assert db_result is not None, "DB에 데이터가 없습니다"
        assert db_result['email'] == user_email, "DB에 저장된 이메일과 API에 등록된 데이터가 다릅니다."
        assert db_result['status'] == 'ACTIVE'

        print(f"[DB] 적재 확인 완료 최종 확인 이메일: {db_result['email']}")
        print("e2e 테스트 완료")