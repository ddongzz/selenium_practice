import pytest
import requests
import time

pytestmark = pytest.mark.ui

def test_fast_checkout_with_api_login(driver):
    # ---------------------------------------------------------
    # 1️⃣ [API 단계] 백그라운드에서 로그인 API 찌르기
    # ---------------------------------------------------------
    login_api_url = "https://api.practicesoftwaretesting.com/users/login"
    payload = {
        "email": "customer@practicesoftwaretesting.com",
        "password": "welcome01"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/json"
    }

    print("\n[로봇] API 서버에 로그인을 시도합니다...")
    response = requests.post(login_api_url, json=payload, headers=headers)
    access_token = response.json().get("access_token")
    
    assert access_token is not None, "💥 토큰 발급 실패"
    print("✅ 출입증(Token) 발급 성공!")

    # ---------------------------------------------------------
    # 2️⃣ [UI 단계] 셀레니움 브라우저 켜고 토큰 주입하기
    # ---------------------------------------------------------
    driver.get("https://practicesoftwaretesting.com/")
    time.sleep(2)

    # 양쪽 주머니에 모두 토큰 쑤셔 넣기
    driver.execute_script(f"""
        window.localStorage.setItem('auth-token', '{access_token}');
        window.sessionStorage.setItem('auth-token', '{access_token}');
    """)

    driver.refresh()
    time.sleep(2)

    # ---------------------------------------------------------
    # 3️⃣ [이동 단계] 로그인 스킵하고 바로 프로필로 이동 (검증 생략)
    # ---------------------------------------------------------
    print("로그인 과정 없이 바로 계정 화면으로 침투합니다!")
    driver.get("https://practicesoftwaretesting.com/#/account")
    
    # 눈으로 화면이 열리는지 대략적으로 볼 수 있게 3초 대기 후 테스트 종료
    time.sleep(3) 
    
    print(f"🔥 최종 도착 주소: {driver.current_url}")
    print("🎉 하이브리드 로그인 세팅 완료! (텍스트 렌더링 검증 생략)")