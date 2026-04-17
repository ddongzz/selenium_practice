import requests
import pytest

# 업데이트를 먼저하기 위해 함수명 변경
def test_1_update_user(api_context, temp_user):
    print("유저 정보 수정 테스트 시작")
    target_id = temp_user
    requests_url = f"{api_context['url']}/{target_id}"

    payload = {
        "name": "Dongchan Lee",
        "job": "Senior QA Engineer"
    }

    response = requests.put(
        requests_url,
        json=payload,
        headers=api_context["headers"]
    )

    assert response.status_code == 200
    data = response.json()
    assert data["job"] == "Senior QA Engineer"
    print(f"상태코드 200 확인 완료 타겟 ID > {target_id} 수정완료")