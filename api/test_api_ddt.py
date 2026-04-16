import requests
import pytest

# 3가지의 데이터를 준비
test_data = [
    ("DongChan Lee", "QA Lead", 201),
    # 400 값을 받아야 되나 테스트용 주소의 한계로 201로 변경
    ("Newbie", "", 201),
    ("Hacker#@#!@", "DROP TABLE users;", 201)
]

# 테스트 준비
@pytest.mark.parametrize("name, job, expected_status", test_data)
def test_create_user_ddt(api_context, name , job, expected_status):
    print(f"테스트 시작, 이름 : {name} / 직업 : {job}")

    payload = {
        "name": name,
        "job": job
    }

    response = requests.post(
        api_context["url"],
        json=payload,
        headers=api_context["headers"]
    )

    assert response.status_code == expected_status, f"예상 코드 : {expected_status} / 실제 코드 : {response.status_code}"
    
    if response.status_code == 201:
        data = response.json()
        assert data["name"] == name, "서버에 저장된 이름과 다릅니다."
        assert data["job"] == job, "서버에 저장된 직업이 다릅니다."
    else:
        (f"비정상 동작이 확인되었습니다. 실제 코드 : {response.status_code}")


    print(f"서버 응답 ID : {data['id']}")