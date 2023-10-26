import time
import os
import sys
from pathlib import Path
import settings
from selenium.webdriver.common.by import By
from service.Driver import Driver, ManagePage
from utils.utils import get_urls_for_parsing, send_data_to_server


NAME = 'otzovik'

class BaseParser(ManagePage, Driver):
    pass


class Parser(BaseParser):
    def __init__(self):
        super().__init__()
        self.driver = self.get_driver()
        self.result = {
            "parser": NAME,
            "data": []
        }


    def new_driver(self):
        return self.get_driver()
    def start(self):
        self.get_data()
        self.driver.close()
        #exit(1)
        print(self.result)
        send_data_to_server(self.result)
    def get_data(self):
        urls = get_urls_for_parsing(parser=NAME)

        for url in urls:
            for key, value in url.items():

                self.driver.get(value)
                raiting = self.get_raiting()
               	#self.driver.get(value)
                count_comments = self.count_comments()
                recommend = self.get_recommend()
                statistics: dict = {
                    key: {
                    'raiting': raiting.split(":")[1].strip(),
                    'count_comments': count_comments.strip(),
                    'recommend': recommend
                    }
                }
                print(statistics)
                self.result["data"].append(statistics)
                time.sleep(10)
                self.driver = self.new_driver()


    def get_raiting(self):
        locator = (By.CLASS_NAME, 'product-rating')
        raiting = self.load_element(locator)
        if not raiting:
            self.driver = self.get_driver()
        raiting = raiting.get_attribute('title')
        return raiting
    def count_comments(self):
        locator = (By.CLASS_NAME, 'reviews-counter')
        elements = self.load_all_elements(locator)
        for element in elements:
            if 'Всего отзывов' in element.text:
                text = element.text.split(":")[1]
                return text
    def get_recommend(self):
        locator = (By.CLASS_NAME, 'recommend-ratio')
        element = self.load_element(locator)
        recommend = element.text.split()[-1]
        return recommend