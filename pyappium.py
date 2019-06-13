# -*- conding:utf-8 -*-
__author__ = "snake"

"""
    Appium的二次封装
"""

from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class Config():
    """
        AppiumDesktop测试配置文件
    """
    LEIDIAN_API_DESIRED_CAPS = {
        "platformName":'Android', 
        "platformVersion":"5.1.1", 
        "deviceName":"vivo x6plus", 
        "appPackage":"io.appium.android.apis", 
        "appActivity":".ApiDemos", 
        "automationName": "UIAutomator2",
        "unicodeKeyboard": True, 
        "resetKeyboard": True
    }

    LEIDIAN_ZHIHU_DESIRED_CAPS = {
        "platformName":'Android', 
        "platfrmVersion":"5.1.1", 
        "deviceName":"vivo x6plus", 
        "appPackage":"com.zhihu.android", 
        "appActivity":".app.ui.activity.MainActivity", 
        "automationName": "UIAutomator2",
        "unicodeKeyboard": True, 
        "resetKeyboard": True
    }

    
    M1NOTE_API_DESIRED_CAPS = {
        "platformName":'Android', 
        "platfrmVersion":"5.1", 
        "deviceName":"m1note", 
        "appPackage":"io.appium.android.apis", 
        "appActivity":".ApiDemos", 
        "automationName": "UIAutomator2",
        "unicodeKeyboard": True, 
        "resetKeyboard": True
    }

    M1NOTE_SCMCC_DESIRED_CAPS = {
        "platformName":'Android', 
        "platfrmVersion":"5.1", 
        "deviceName":"m1note", 
        "appPackage":"com.sunrise.scmbhc", 
        "appActivity":".ui.activity.home.HomeActivity", 
        "automationName": "UIAutomator2",
        "unicodeKeyboard": True, 
        "resetKeyboard": True
    }

class PyAppium():
    """
        AppiumDriver二次封装
    """
    def __init__(self, url="http://localhost:4723/wd/hub", desired_caps={}, timeout=10):
        """
            构造方法
        """
        self._driver = webdriver.Remote(url, desired_caps)
        self._timeout = timeout

    def get_origina_driver(self):
        """
            获取appium原始的driver
        """
        return self._driver

    def find_element(self, locator):
        """
            查找单个元素
            参数：
                id: "id"
                xpath: "xpath"
                accessibility_id: "aid"
                android_uiautomator: "aui"
        """
        if not isinstance(locator, tuple) or len(locator) != 2:
            raise Exception("输入的参数必须是(by, value)格式!")

        # 简写
        if locator[0] == "aid":
            locator = (MobileBy.ACCESSIBILITY_ID, locator[1])
        if locator[0] == "aui":
            locator = (MobileBy.ANDROID_UIAUTOMATOR, locator[1])

        try:
            return WebDriverWait(self._driver, self._timeout).until(lambda s: s.find_element(*locator))
        except:
            raise Exception("未找到元素{}!".format(locator))

    def find_elements(self, locator):
        """
            查找多个元素
            参数：
                id: "id"
                xpath: "xpath"
                accessibility_id: "aid"
                android_uiautomator: "aui"
        """
        if not isinstance(locator, tuple) or len(locator) != 2:
            raise Exception("输入的参数必须是(by, value)格式!")

        # 简写
        if locator[0] == "aid":
            locator = (MobileBy.ACCESSIBILITY_ID, locator[1])
        if locator[0] == "aui":
            locator = (MobileBy.ANDROID_UIAUTOMATOR, locator[1])

        try:
            return WebDriverWait(self._driver, self._timeout).until(lambda s: s.find_elements(*locator))
        except:
            raise Exception("未找到元素{}!".format(locator))

    def type_zh(self, locator, keywords):
        """
            支持中文的输入
        """
        self.find_element(locator).send_keys(keywords)

    def type(self, locator, keywords):
        """
            快速的输入，不支持中文
        """
        self._driver.set_value(self.find_element(locator), keywords)

    def click(self, locator):
        """
            点击操作
        """
        self.find_element(locator).click()

    def switch_to_alert(self):
        """
            appium作用域切换到alert
        """
        self._driver.switch_to_alert()

    def switch_to_default_content(self):
        """
            appium切换到默认作用域
        """
        self._driver.switch_to_default_content()

    def does_exist(self, locator):
        """
            动态判断元素是否存在
                - 元素存在：True
                - 元素不存在：False
        """
        try:
            self.find_element(locator)
            return True
        except:
            return False
            
    def does_toast_exist(self, text=None):
        """
            根据toast文本判断toast是否存在
                - 存在返回：元素, True
                - 不存在返回：None, False
            注意: 此方法需要指定启动参数 "automationName": "UIAutomator2" !
        """
        try:
            toast_loc = ("xpath", ".//*[contains(@text,'{}')]".format(text))
            e = self.find_element(toast_loc)
            return e, True
        except:
            return None, False


if __name__ == "__main__":
    # desired_caps = {}
    # desired_caps['platformName'] = 'Android'                    # 打开什么平台的app，固定的 > 启动安卓平台
    # desired_caps['platformVersion'] = '5.1.1'                   # 安卓系统的版本号：adb shell getprop ro.build.version.release
    # desired_caps['deviceName'] = 'vivo x6plus d'                # 手机/模拟器的型号：adb shell getprop ro.product.model
    # desired_caps['appPackage'] = 'io.appium.android.apis'       # app的名字：adb shell dumpsys activity | findstr "mFocusedActivity"
    # desired_caps['appActivity'] = '.ApiDemos'                   # app的启动页名字：adb shell dumpsys activity | findstr "mFocusedActivity"
    # desired_caps['unicodeKeyboard'] = True                      # 为了支持中文
    # desired_caps['resetKeyboard'] = True                        # 设置成appium自带的键盘
    # pyappium = PyAppium(desired_caps=desired_caps)

    pyappium = PyAppium(desired_caps=Config.M1NOTE_API_DESIRED_CAPS)

    # 1. 查找元素的用法
    # locator = ("id", "android:id/text1") 
    # locator = ("xpath", '//android.widget.TextView[@content-desc="Accessibility"]')
    # locator = ("aid", "Accessibility")
    # locator = ("aui", 'new UiSelector().text("Accessibility")')
    # pyappium.find_element(locator).click()

    # 2. 操作元素
    app = ("aid", "App")
    app_search = ("aid", "Search")
    app_search_invoke = ("aid", "Invoke Search")
    app_search_invoke_appdata = ("id", "io.appium.android.apis:id/txt_query_appdata")

    pyappium.click(app)
    pyappium.click(app_search)
    pyappium.click(app_search_invoke)
    pyappium.type(app_search_invoke_appdata, "hello appium!")
    pyappium.type_zh(app_search_invoke_appdata, "hello appium!")

    print(pyappium.does_exist(app))
