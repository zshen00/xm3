from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def loginWeb():
    driver = webdriver.Chrome()
    driver.get("http://47.96.3.9:8080/subwayweb/")
    print(driver.title)
    userID = WebDriverWait(driver, 10, 0.5).until(
                          EC.presence_of_element_located((By.CSS_SELECTOR, "#userId"))
                          )
    userPass =WebDriverWait(driver, 10, 0.5).until(
                          EC.presence_of_element_located((By.CSS_SELECTOR, "#password"))
                          )
    pSubmit = WebDriverWait(driver, 10, 0.5).until(
                          EC.element_to_be_clickable((By.CSS_SELECTOR, "#box > div > table > tbody > tr:nth-child(3) > td:nth-child(2) > input"))
                          )

    userID.send_keys('ipuser')
    userPass.send_keys('qaz123')
    pSubmit.click()

    driver.implicitly_wait(10)
    driver.get("http://47.96.3.9:8080/subwayweb/jsp/paramManage/agmParmManage.jsp")
    print(driver.title)
    driver.maximize_window()

    return driver