from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import time

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
    submit = WebDriverWait(driver, 10, 0.5).until(
                          EC.element_to_be_clickable((By.CSS_SELECTOR, "#box > div > table > tbody > tr:nth-child(3) > td:nth-child(2) > input"))
                          )

    userID.send_keys('ipuser')
    userPass.send_keys('qaz123')
    submit.click()

    driver.implicitly_wait(10)
    driver.get("http://47.96.3.9:8080/subwayweb/jsp/paramManage/agmParmManage.jsp")

    print(driver.title)

    driver.maximize_window()

    time.sleep(1)
    return driver

def checkPage(driver):
    try:
        pDeviceState = driver.find_elements_by_xpath('//td[@field="speechV"]/div')
        pDevicesID = driver.find_elements_by_xpath('//td[@field="deviceNo"]/div')
        pStationName = driver.find_elements_by_xpath('//td[@field="stationName"]/div')
        pDeviceName = driver.find_elements_by_xpath('//td[@field="deviceName"]/div')
        i = 0
        for index in pDeviceState:
            text1 = index.text
            if (text1.find('PCM') > 0 or text1.find('停止') > 0):
                DevicesID = pDevicesID[i]
                StationName = pStationName[i]
                DeviceName = pDeviceName[i]
                print('---------------------------------------------------> '
                      +DevicesID.text + ' ' + StationName.text + ' ' + DeviceName.text + ' ' + index.text )
            elif text1.find('异常') > 0:
                DevicesID = pDevicesID[i]
                StationName = pStationName[i]
                DeviceName = pDeviceName[i]
                print(DevicesID.text + ' ' + StationName.text + ' ' + DeviceName.text + ' ' + index.text)
            else:
                t = 0
            i = i + 1
    except:
        print('err')
        return 0
    else:return 1


def checkFault(totalPage):
    page = 1
    while (page <= totalPage):
        pageNumber = driver.find_element_by_css_selector(
            "body > div.panel.layout-panel.layout-panel-center > div > div > div > div.datagrid-pager.pagination > table > tbody > tr > td:nth-child(7) > input")
        pageNumber.clear()
        pageNumber.send_keys(page)
        pageNumber.send_keys(Keys.ENTER)
        time.sleep(2)
        fun=checkPage(driver)
        while fun != 1:
            fun=checkPage(driver)

        page = page + 1

driver =loginWeb()
selectClick = driver.find_element_by_css_selector("#formA > table > tbody > tr > td:nth-child(8) > span > span")
ActionChains(driver).move_to_element(selectClick).perform()
time.sleep(1)
selectClick.click()
time.sleep(1)
selectClick = driver.find_element_by_css_selector("body > div.panel.combo-p > div > div:nth-child(3)")
selectClick.click()
time.sleep(1)

submit=driver.find_element_by_css_selector("#formA > table > tbody > tr > td:nth-child(9) > a")
submit.click()

driver.implicitly_wait(10)
selectNumber = driver.find_element_by_css_selector("body > div.panel.layout-panel.layout-panel-center > div > div > div > div.datagrid-pager.pagination > table > tbody > tr > td:nth-child(1) > select")
Select(selectNumber).select_by_index(2)
time.sleep(1)

totalPageText =  driver.find_element_by_css_selector("body > div.panel.layout-panel.layout-panel-center > div > div > div > div.datagrid-pager.pagination > table > tbody > tr > td:nth-child(8) > span").text
print(totalPageText)
totalPage= int(totalPageText[1:-1])
print(totalPage)

i=0
while (i<12):
    checkFault(totalPage)
    print("===========================================%d===="%i,end=" ")
    print (time.strftime(" %H:%M", time.localtime()))
    i=i+1
    time.sleep(3)

driver.quit()