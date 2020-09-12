from os import system
from collections import OrderedDict
import time
from time import strftime, gmtime

from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException

from form_filler_base import FormFillerBase


class EducationGanFormFiller(FormFillerBase):
    def __init__(self):
        self._url = r'https://parents.education.gov.il/prhnet/parents/rights-obligations-regulations/health-statement-kindergarden'
        super().__init__(height_buffer=1500)

        self._xpaths=OrderedDict({
            'fill_request': '//*[@id="main-content"]/section[1]/div/health-declaration/div/div[1]/div[4]/div/div/div/input',
            'user_name': '//*[@id="HIN_USERID"]',
            'password': '//*[@id="Ecom_Password"]',
            'submit_login': '//*[@id="loginButton2"]'
        })

    def _fill_form(self, form_fields, submit=False):
        self._click_field('fill_request')
        time.sleep(3)
        self._fill_field('user_name', '4135457')
        self._fill_field('password', '9921')
        self._click_field('submit_login')

class EducationWebTopFormFiller(FormFillerBase):
    def __init__(self):
        self._url = r'https://www.webtop.co.il/v2/?'
        super().__init__(height_buffer=500, headless=False)

        self._xpaths=OrderedDict({
            'login_click': '//*[@id="restorePassword"]/input[2]',
            'user_name': '//*[@id="HIN_USERID"]',
            'password': '//*[@id="Ecom_Password"]',
            'submit_login': '//*[@id="loginButton2"]',
            'parent_id': '//*[@id="signerID"]',
            'submit': '//*[@id="saveButton"]',
            'qr_code': '//*[@id="qrCodeButton"]',
            'iframe1': '//*[@id="window_2_iframe"]',
            'close': '//*[@id="window_2"]/div/table/tbody/tr/td[6]/img',
            'close2': '//*[@id="window_alert"]/div/table/tbody/tr/td[6]/img',
            'iframe': "//*[@id='window_63_iframe']",
        })

    def _fill_form(self, form_fields, submit=False):
        self._click_field('login_click')
        time.sleep(3)
        handles = self._driver.window_handles
        self._driver.switch_to.window(handles[1])
        self._fill_field('user_name', form_fields['user_name'])
        self._fill_field('password', form_fields['password'])
        self._click_field('submit_login')
        time.sleep(1)
        self._driver.switch_to.window(handles[0])
        self._click_field('close')
        self._click_field('close2')

        iframe = self._driver.find_element_by_xpath(self._xpaths['iframe'])
        self._driver.switch_to.frame(iframe)
        self._fill_field('parent_id', form_fields['parent_id'])
        # self._save_snapshot(form_fields['parent_name'], 'filled_form')

        # submit
        if submit:
            self._click_field('submit')
            time.sleep(1)
            try:
                self._driver.switch_to.alert.accept()
            except NoAlertPresentException:
                pass
            time.sleep(3)
            self._save_snapshot(form_fields['parent_name'], 'submit_form')
            self._click_field('qr_code')
            time.sleep(3)

            self._save_snapshot(form_fields['parent_name'], 'qr_code')


if __name__ == '__main__':
    # EducationGanFormFiller().fill_form({})
    EducationWebTopFormFiller().fill_form({})
