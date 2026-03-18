from selenium.webdriver.common.by import By

class LoginPage:
    # 화면요소에 대한것을 정리한다. 나중에 해당 값이 바뀔 경우 해당 파일에서만 수정하면된다.
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # 초기 값, 봇이 사용할 수 있도록 해주는 기본 세팅
    def __init__(self, driver):
        self.driver = driver

    # 행동을 함수로 생성
    def login(self, username, password):
        # 아이디와 비밀번호를 받고 로그인 버튼을 클릭하는 행동
        self.driver.find_element(*self.USERNAME_INPUT).clear()
        if username:
            self.driver.find_element(*self.USERNAME_INPUT).send_keys(username)

        self.driver.find_element(*self.PASSWORD_INPUT).clear()
        if password:
            self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def get_error_message(self):
        # 에러메시지의 텍스트를 받아오는 행동
        return self.driver.find_element(*self.ERROR_MESSAGE).text