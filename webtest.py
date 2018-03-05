from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from webinit import loginWeb
import winsound
import time
from postWx import wxLogin
from postWx import wxPutTxt

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
                textPut = DevicesID + ' ' + StationName + ' ' + DeviceName + '    ' + DeviceState
                wxPutTxt(textPut)
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


# 登录微信
wxLogin()
wxPutTxt("测试")


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
i = 0
n = 48
while (i < n):
    checkFault(totalPage)
    print("===========================================%d===="%i, end=" ")
    print(time.strftime(" %H:%M", time.localtime()))
    print()
    wxPutTxt(i)
    i=i+1
    #最后一次检查完不等待
    if i < n:
        time.sleep(300)
winsound.Beep(697, 200), winsound.Beep(697, 200), winsound.Beep(697, 200)
driver.quit()
wxPutTxt('结束了')