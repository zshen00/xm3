from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
import winsound
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

def checkPage(driver):
    # 检查一个页面内的故障
    try:
        pDeviceState = driver.find_elements_by_xpath('//td[@field="speechV"]/div')
        pDevicesID = driver.find_elements_by_xpath('//td[@field="deviceNo"]/div')
        pStationName = driver.find_elements_by_xpath('//td[@field="stationName"]/div')
        pDeviceName = driver.find_elements_by_xpath('//td[@field="deviceName"]/div')
        i = 0
        for index in pDeviceState:
            DeviceState = index.text
            if (DeviceState.find('PCM') > 0 or DeviceState.find('停止') > 0):
                DevicesID = pDevicesID[i].text
                StationName = pStationName[i].text
                DeviceName = pDeviceName[i].text
                DeviceName = DeviceName.replace(' ', '')
                print('                                          ---------> '
                      +DevicesID + ' ' + StationName + ' ' + DeviceName + '    ' + DeviceState )
                winsound.Beep(880, 300), winsound.Beep(807, 600)
            elif DeviceState.find('异常') > 0:
                DevicesID = pDevicesID[i].text
                StationName = pStationName[i].text
                DeviceName = pDeviceName[i].text
                print(DevicesID + ' ' + StationName + ' ' + DeviceName + ' ' + DeviceState)
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

# 登陆查询页面
driver =loginWeb()

# 选择参数
# 选择AGM
selectClick = driver.find_element_by_css_selector("#formA > table > tbody > tr > td:nth-child(8) > span > span")
ActionChains(driver).move_to_element(selectClick).perform()
time.sleep(1)
selectClick.click()
time.sleep(1)
selectClick = driver.find_element_by_css_selector("body > div.panel.combo-p > div > div:nth-child(3)")
selectClick.click()
time.sleep(1)

# 点击查询
submit=driver.find_element_by_css_selector("#formA > table > tbody > tr > td:nth-child(9) > a")
submit.click()

# 选择每页显示30条
driver.implicitly_wait(10)
selectNumber = driver.find_element_by_css_selector("body > div.panel.layout-panel.layout-panel-center > div > div > div > div.datagrid-pager.pagination > table > tbody > tr > td:nth-child(1) > select")
Select(selectNumber).select_by_index(2)
time.sleep(1)

totalPageText =  driver.find_element_by_css_selector("body > div.panel.layout-panel.layout-panel-center > div > div > div > div.datagrid-pager.pagination > table > tbody > tr > td:nth-child(8) > span").text
print(totalPageText)
totalPage= int(totalPageText[1:-1])

# 循环进行24次检查，每次间隔5分钟
i=0
while (i<24):
    checkFault(totalPage)
    print("===========================================%d===="%i, end=" ")
    print(time.strftime(" %H:%M", time.localtime()))
    print()
    i=i+1
    #最后一次检查完不等待
    if i < 24:
        time.sleep(300)
    winsound.Beep(697, 200), winsound.Beep(697, 200), winsound.Beep(697, 200)
driver.quit()