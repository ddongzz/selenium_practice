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
    new_user_id = response.json()['id']

    # DB 넣기 
    with db_connection.cursor() as cursor:
        cursor.execute("CREATE TABLE IF NOT EXISTS real_users(id VARCHAR(50), name VARCHAR(50), job VARCHAR(50))")
        cursor.execute("INSERT INTO real_users (id, name, job) VALUES(%s, %s, %s)", (new_user_id, payload['name'], payload['job']))
        db_connection.commit()

    # 넣은 DB 확인하기
    with db_connection.cursor() as cursor:
        cursor.execute("SELECT * FROM real_users WHERE id = %s", (new_user_id,))
        db_result = cursor.fetchone()

    assert db_result is not None
    assert db_result['name'] == payload['name']


