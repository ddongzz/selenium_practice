import requests

print("파이썬 API 자동화 테스트 시작!\n")

# ==========================================
# 1. Path Variable (경로 변수) - 1번 유저 지목
# ==========================================
print("=== 1. Path Variable 테스트 (GET) ===")
url_path = "https://jsonplaceholder.typicode.com/users/1"
response_path = requests.get(url_path)

print(f"응답 상태 코드: {response_path.status_code}")
# 응답받은 데이터(JSON) 중에서 'name' 값만 쏙 뽑아서 출력해봅니다.
print(f"가져온 유저 이름: {response_path.json()['name']}\n")


# ==========================================
# 2. Query Parameter (조건 검색) - 1번 유저의 글만
# ==========================================
print("=== 2. Query Parameter 테스트 (GET) ===")
url_query = "https://jsonplaceholder.typicode.com/posts"
query_data = {"userId": 1}
response_query = requests.get(url_query, params=query_data)

print(f"응답 상태 코드: {response_query.status_code}")
# 리스트 형태로 오기 때문에 len() 함수로 몇 개인지 세어봅니다.
print(f"가져온 게시글 개수: {len(response_query.json())}개\n")


# ==========================================
# 3. Request Body (생성) - 정상 데이터 전송
# ==========================================
print("=== 3. Request Body 정상 테스트 (POST) ===")
url_body = "https://jsonplaceholder.typicode.com/posts"
good_payload = {
    "title": "파이썬 자동화 테스트",
    "body": "코드로 쏘니까 한 방에 되네요!",
    "userId": 1
}
response_body = requests.post(url_body, json=good_payload)

print(f"응답 상태 코드: {response_body.status_code}")  # 201 Created 예상
print(f"서버가 응답한 데이터: {response_body.json()}\n")


# ==========================================
# 4. Request Body (예외 테스트) - 이상한 데이터 전송
# ==========================================
print("=== 4. Request Body 예외 테스트 (POST) ===")
bad_payload = {
    "title": "",            # 필수값 누락
    "userId": "문자열입니다"  # 데이터 타입 오류
}
response_bad = requests.post(url_body, json=bad_payload)

print(f"응답 상태 코드: {response_bad.status_code}")
if response_bad.status_code == 201:
    print("QA 포인트: 가짜 서버라서 예외 데이터도 201(성공) 처리해 버렸습니다. (실무였다면 방어 로직 누락 버그!)")
else:
    print("서버가 이상한 데이터를 정상적으로 차단했습니다.")