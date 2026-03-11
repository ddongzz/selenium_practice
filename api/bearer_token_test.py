import requests

url = "https://httpbin.org/bearer"

print("=== 1. 토큰 없이 무단 침입 시도 (Negative Test) ===")
# 헤더 없이 그냥 냅다 찔러봅니다.
response_fail = requests.get(url)

print(f"응답 상태 코드: {response_fail.status_code}")
if response_fail.status_code == 401:
    print("[401 Unauthorized] 삐빅! 출입증이 없어서 쫓겨났습니다.\n")


print("=== 2. 토큰 챙겨서 당당하게 입장 (Positive Test) ===")
# 가짜 JWT 토큰을 하나 발급받았다고 칩시다.
my_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.dummy_token_payload.1234567890"

# 여기가 핵심! 헤더(headers) 딕셔너리에 Bearer 양식으로 세팅합니다.
# 주의: Bearer 띄우고 토큰값입니다!
auth_headers = {
    "Authorization": f"Bearer {my_token}"
}

# 요청할 때 headers 옵션에 딕셔너리를 넘겨줍니다.
response_success = requests.get(url, headers=auth_headers)

print(f"응답 상태 코드: {response_success.status_code}")
if response_success.status_code == 200:
    print("[200 OK] 출입증 확인 완료! 문이 열렸습니다.")
    print(f"서버가 확인한 내 정보: {response_success.json()}")