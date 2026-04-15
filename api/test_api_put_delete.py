import requests
import pytest

# 업데이트를 먼저하기 위해 함수명 변경
def test_1_update_user(api_context):
    print("API PUT 테스트 시작")

    request_url = f"{api_context['url']}"

    payload = {
        "name": "Dongchan Lee",
        "job": "Senior QA Engineer"
    }
    
    response = requests.put(
        request_url, 
        json=payload, 
        headers=api_context["headers"]
    )

    assert response.status_code == 200, f"데이터 수정 실패 : {response.status_code}"
    print("데이터 수정 완료")
    
    data = response.json()
    assert data["job"] == "Senior QA Engineer", "직업이 변경되지 않았습니다."
    print(f"데이터 수정 확인 : {data['job']} 업데이트 시간 : {data['updatedAt']}")

def test_2_delete_user(api_context):
    print("데이터 삭제 시작")

    request_url = f"{api_context['url']}/2"

    response = requests.delete(
        request_url, 
        headers=api_context["headers"]
    )

    # 삭제가 되었는지 알아보는 코드 204
    assert response.status_code == 204, f"데이터 삭제가 되지 않았습니다.{response.status_code}"
    print("데이터 삭제 완료")