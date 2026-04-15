import requests
import pytest

def test_create_new_user(api_context):
    print("API POST 테스트 시작")

    payload = {
        "name": "Dongchan Lee",
        "job": "QA Engineer"
    }

    response = requests.post(
        api_context["url"],
        json=payload,
        headers=api_context["headers"]
    )
        

    assert response.status_code == 201, f"데이터 생성 실패 : {response.status_code}"
    print("데이터 생성 201 성공")

    data = response.json()
    print(f"서버 응답 데이터: {data}")

    assert data["name"] == "Dongchan Lee", "이름이 같지 않습니다."
    assert data["job"] == "QA Engineer", "직업이 같지 않습니다."
    assert "id" in data, "고유 ID가 발급되지 않았습니다."

    print(f"서버가 부여한 ID : {data['id']}")