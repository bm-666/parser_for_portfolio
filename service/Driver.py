import settings
from settings import manifest_json, background_js
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_user_agent import user_agent
import zipfile
from loguru import logger



class Driver:
    def __init__(self):
        self.driver = self.__init_driver()

    def get_driver(self):
        return self.driver

    def  __init_driver(self):
        use_proxy = True
        options = webdriver.ChromeOptions()
        ua = user_agent()
        if use_proxy:
            pluginfile = 'proxy_auth_plugin.zip'

            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
            options.add_extension(pluginfile)

        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2,
         })

        #options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--headless=new")
        #options.add_argument('start-maximized')
        #options.add_argument('enable-automation')
        #options.add_argument('--disable-dev-shm-usage')
        #options.add_argument('--dns-prefetch-disable')
        #options.add_argument("--disable-extensions")
        #options.add_argument('--disable-infobars')
        #options.add_argument('--disable-gpu')
        ua = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0'
        options.add_argument(f'user-agent={ua}')
        #options.add_argument("--disable-dev-shm-usage")
        #options.add_experimental_option("excludeSwitches", ["enable-automation"])
        #options.add_experimental_option("useAutomationExtension", False)
        # options.add_argument(f"proxy-server={self.proxy_server}")


        driver: webdriver = webdriver.Chrome(
            options=options
        )
        #driver.add_cookie({"name":"refreg", "value":"1694270127~"})
        #driver.add_cookie({"name": "ROBINBOBIN", "value": "862fb930b8360200be7402d971"})
        #driver.add_cookie({"name": "ssid", "value": "362187547"})

        driver.set_window_size(1920, 1080)
        return driver
class ManagePage:
    timeout = 20

    def load_element(self, locator):
        element = None
        try:
            element = WebDriverWait(self.driver, self.timeout).until(EC.presence_of_element_located(locator))
        except Exception:
            logger.error('Not found element')

        return element
    def load_all_elements(self, locator):
        elements = None
        try:
            elements = WebDriverWait(self.driver, self.timeout).until(EC.presence_of_all_elements_located(locator))
        except Exception:
            logger.error('Not found elements')
        return elements

