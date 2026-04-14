import requests
import pytest

def test_get_user_list():
    print("API 요청 테스트 시작")

    url = "https://reqres.in/api/users?page=2"
    headers = {
        "x-api-key": "pub_46acecc3066bc0da2b0f3f19aa63d77ad99e1bfb052def73453ce1af06382153"
    }
    response = requests.get(url, headers=headers)

    print("상태코드 200 확인")

    data = response.json()

    assert data["page"] == 2, "요청한 페이지번호와 응답 데이터가 다릅니다."
    assert len(data["data"]) > 0, "유저 데이터가 없습니다."

    print(f"유저의 데이터가 조회되었습니다. 총 {len(data['data'])}명의 유저가 조회되었습니다.")

    first_user_email = data['data'][0]['email']
    print(f"첫번째 유저의 이메일 : {first_user_email}")