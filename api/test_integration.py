import requests
import pytest

def test_create_user_and_verify_db(api_context, db_connection):
    # API로 데이터 생성 요청
    payload = {
        "name": "Dongchan Lee",
        "job": "QA Lead"
    }
    response = requests.post(
        api_context["url"],
        json=payload,
        headers=api_context["headers"]
    )

    assert response.status_code == 201, "201 값이 아닙니다."
    api_data = response.json()
    new_user_id = api_data['id']
    print(f"API 생성 완료, 발급된 ID : {new_user_id}")

    # 서버가 없어 데이터베이스를 직접 넣어준다.

    with db_connection.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS real_users (id VARCHAR(50), name VARCHAR(50), job VARCHAR(50))")
        cursor.execute(
            "INSERT INTO real_users (id, name, job) VALUES (%s, %s, %s)",
            (new_user_id, api_data['name'], api_data['job'])
        )
        db_connection.commit()

    # 추가한 데이터 확인
    print(f"생성한 데이터 확인 : {new_user_id}")

    with db_connection.cursor() as cursor:
        # API에서 응답받은 ID로 DB를 조회
        sql = "SELECT * FROM real_users WHERE ID = %s"
        cursor.execute(sql, (new_user_id,))

        # 조건에 맞는 데이터 1줄 가져오기
        db_result = cursor.fetchone()

    # 데이터가 있는지 확인
    assert db_result is not None, "DB에 데이터에 저장되지 않았습니다."
    print("데이터 조회 성공")

    # 정합성 크로스 체크
    assert db_result['name'] == payload['name'], f"값이 일치하지 않습니다.{db_result['name']}, {payload['name']}"
    assert db_result['job'] == payload['job'], f"값이 일치하지 않습니다.{db_result['job'], {payload['job']}}"

    print("최종 결과가 일치합니다.")


