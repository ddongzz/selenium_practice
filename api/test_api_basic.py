import requests
import pytest

def test_get_user_list(api_context):
    print("API 요청 테스트 시작")

    # conftest.py에서 배달받은 url에 쿼리 파라미터만 추가
    request_url = f"{api_context['url']}?page=2"
    
    # 배달받은 headers 적용
    response = requests.get(request_url, headers=api_context["headers"])

    print("상태코드 200 확인")

    data = response.json()

    assert data["page"] == 2, "요청한 페이지번호와 응답 데이터가 다릅니다."
    assert len(data["data"]) > 0, "유저 데이터가 없습니다."

    print(f"유저의 데이터가 조회되었습니다. 총 {len(data['data'])}명의 유저가 조회되었습니다.")

    first_user_email = data['data'][0]['email']
    print(f"첫번째 유저의 이메일 : {first_user_email}")