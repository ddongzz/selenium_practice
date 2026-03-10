import requests

# 프로세스를 이해하기 위한 코드

# print("실전 API 로그인 및 토큰 인증 시나리오 시작!\n")

# # ==========================================
# # STEP 1. 로그인하고 JWT 토큰 발급받기
# # ==========================================
# print("1. 로그인 요청을 보냅니다...")
# login_url = "https://dummyjson.com/auth/login"

# # 이 테스트 서버에 미리 등록되어 있는 테스트용 계정입니다.
# login_payload = {
#     "username": "emilys",
#     "password": "emilyspass"
# }

# login_res = requests.post(login_url, json=login_payload)

# # 로그인이 성공(200)했을 때만 다음 단계로 넘어갑니다.
# if login_res.status_code == 200:
#     print("[성공] 로그인 성공!")
    
#     # 응답받은 JSON 데이터에서 'accessToken' 이라는 키의 값(토큰)만 쏙 뽑아냅니다.
#     my_token = login_res.json()['accessToken']
#     print(f"[토큰] 서버가 준 토큰: {my_token[:30]}... (너무 길어서 생략)\n")
    
#     # ==========================================
#     # STEP 2. 발급받은 토큰으로 '내 정보' 접근하기
#     # ==========================================
#     print("2. 방금 받은 토큰을 출입증으로 써서 내 정보 조회를 요청합니다...")
#     my_info_url = "https://dummyjson.com/auth/me"
    
#     # 헤더에 Authorization 키를 만들고 "Bearer 토큰값" 형태로 세팅합니다.
#     auth_headers = {
#         "Authorization": f"Bearer {my_token}"
#     }
    
#     # 요청할 때 파라미터가 아니라 headers 옵션에 딕셔너리를 넘깁니다!
#     info_res = requests.get(my_info_url, headers=auth_headers)
    
#     if info_res.status_code == 200:
#         print("[200 OK] 출입증 확인 완료! 정보 조회에 성공했습니다.")
#         # 응답 데이터에서 이름 부분만 추출해서 출력해 봅니다.
#         first_name = info_res.json()['firstName']
#         last_name = info_res.json()['lastName']
#         print(f"[환영] 환영합니다, {first_name} {last_name}님!")
#     else:
#         print(f"[실패] 정보 조회 실패 (상태 코드: {info_res.status_code})")

# else:
#     print(f"[실패] 로그인 실패 (상태 코드: {login_res.status_code})")

# ===============pytest를 위해 수정된 코드=============================

# 1. 로그인 및 토큰 발급 테스트
def test_login_and_get_info():
    # [준비] 로그인 정보
    login_url = "https://dummyjson.com/auth/login"
    login_payload = {
        "username": "emilys",
        "password": "emilyspass"
    }

    # [실행] 로그인 API 호출
    login_res = requests.post(login_url, json=login_payload)
    
    # [검증] 로그인 성공(200)을 기대함
    assert login_res.status_code == 200
    
    # 토큰 추출
    token = login_res.json()['accessToken']
    assert token is not None  # 토큰이 비어있지 않아야 함
    
    # [실행] 내 정보 조회 API 호출
    info_url = "https://dummyjson.com/auth/me"
    headers = {"Authorization": f"Bearer {token}"}
    info_res = requests.get(info_url, headers=headers)
    
    # [검증] 정보 조회 성공(200) 및 이름 확인
    assert info_res.status_code == 200
    assert info_res.json()['firstName'] == "Emily"

# 2. 로그인 실패 케이스 테스트 (일부러 틀린 비번)
def test_login_fail():
    login_url = "https://dummyjson.com/auth/login"
    bad_payload = {
        "username": "emilys",
        "password": "wrong_password"
    }
    
    res = requests.post(login_url, json=bad_payload)
    
    # [검증] 실패했을 때 400 에러를 뱉는지 확인
    assert res.status_code == 400