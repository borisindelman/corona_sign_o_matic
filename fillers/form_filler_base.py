import os
from abc import ABC, abstractmethod
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import selenium.webdriver.chrome as chrome
import platform


class FormFillerBase(ABC):
    def __init__(self, height_buffer = 1000, headless=True):
        self.headless=headless
        self.height_buffer = height_buffer
        self._wait_seconds = 0.2
        self.snapshots = []
        self.expected_snapshots = 0
        self.debug_snapshots = 0
        self.is_temperature_required = False

    def _init_driver(self):
        #chrome_driver_path = os.path.join(os.path.dirname(__file__), '../executables', 'chromedriver')
        chrome_driver_path = 'chromedriver'
        chrome_options = self._init_web_options()
        if platform.system() == 'Windows':
            chrome_driver_path =chrome_driver_path + '.exe'
        self._driver = webdriver.Chrome(executable_path=chrome_driver_path,
                                        chrome_options=chrome_options)

        ele = self._driver.get_window_size()
        total_height = ele['height'] + self.height_buffer
        self._driver.set_window_size(ele['width'], total_height)

    def _init_web_options(self):
        chrome_options = chrome.options.Options()
        if self.headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--lang=en-us')

        return chrome_options

    def fill_form(self, form_fields, submit=False):
        self._init_driver()
        self._driver.get(self._url)
        time.sleep(2)
        self._fill_form(form_fields, submit)
        self._driver.close()
        return self.snapshots

    @abstractmethod
    def _fill_form(self, form_fields, submit=False):
        pass

    def _fill_field(self,xpath:str, value:str):
        time.sleep(self._wait_seconds)
        try:
            self._driver.find_element_by_xpath(self._xpaths[xpath]).send_keys(value)
        except NoSuchElementException:
            return False
        return True


    def _click_field(self, xpath:str):
        time.sleep(self._wait_seconds)
        try:
            self._driver.find_element_by_xpath(self._xpaths[xpath]).click()
        except NoSuchElementException:
            return False
        return True

    def _select_box(self, box_xpath, check_xpath:str):
        time.sleep(self._wait_seconds)
        try:
            if not self._driver.find_element_by_xpath(self._xpaths[box_xpath]).is_selected():
                element = self._driver.find_element_by_xpath(self._xpaths[check_xpath])
                self._driver.execute_script("arguments[0].click();", element)
        except NoSuchElementException:
            return False
        return True

    def _save_snapshot(self, child_name, stage_name):
        file_path = f'screenshot_{child_name}_{stage_name}.png'
        self._driver.get_screenshot_as_file(file_path)
        self.snapshots.append(file_path)


