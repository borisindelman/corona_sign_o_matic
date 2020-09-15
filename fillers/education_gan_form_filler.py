from collections import OrderedDict
import time

from selenium.common.exceptions import NoAlertPresentException

from fillers.form_filler_base import FormFillerBase


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
        self.expected_snapshots = 1
        self.debug_snapshots = 0

    def _fill_form(self, form_fields, submit=False):
        self._click_field('fill_request')
        time.sleep(3)
        self._fill_field('user_name', form_fields['user_name'])
        self._fill_field('password', form_fields['password'])
        time.sleep(3)

        self._click_field('submit_login')
        try:
            self._driver.switch_to.alert.accept()
        except NoAlertPresentException:
            pass
        time.sleep(30)
        self._save_snapshot(form_fields['parent_name'], 'submit_form')
