from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# Chrome 드라이버 자동 설치 및 실행
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://www.google.com")
time.sleep(2)

search_box = driver.find_element(By.NAME, "q")
search_box.send_keys("ChatGPT")
search_box.submit()

time.sleep(3)
print("테스트 완료")
driver.quit()
