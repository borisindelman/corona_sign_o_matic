import pdb
from collections import OrderedDict
import time

import _gdbm
from selenium.common.exceptions import NoAlertPresentException

from fillers.form_filler_base import FormFillerBase


class MashovFormFiller(FormFillerBase):
    def __init__(self):
        self._url = r'https://web.mashov.info/students/login'
        super().__init__(height_buffer=500)

        self._xpaths=OrderedDict({
            'school_name': '//*[@id="mat-input-3"]',
            'school_name_click': '//*[@id="mat-option-82"]/span',
            'year': '//*[@id="mat-select-value-1"]/span',
            'year_click': '//*[@id="mat-option-87"]/span',
            'user': '//*[@id="mat-input-0"]',
            'password': '//*[@id="mat-input-4"]',
            'enter': '//*[@id="mat-tab-content-0-0"]/div/div/button[1]',
            'daily_corona': '//*[@id="mainView"]/mat-sidenav-content/mshv-student-covidsplash/mat-card/mat-card-content/div[3]/mat-card/span',
            'confirm_1_box': '//*[@id="mat-checkbox-1-input"]',
            'confirm_1_check': '//*[@id="mat-checkbox-1"]/label/div/div[1]',
            'confirm_2_box': '//*[@id="mat-checkbox-2-input"]',
            'confirm_2_check': '//*[@id="mat-checkbox-2"]/label/div/div[1]',
            'submit': '//*[@id="mainView"]/mat-sidenav-content/mshv-students-covid-clearance/mat-card/mat-card-actions/button/span[1]'
        })
        self.expected_snapshots = 1
        self.debug_snapshots = 0

    def _fill_form(self, form_fields, submit=False):
        self._fill_field('school_name', form_fields['school_name'])
        self._click_field('school_name_click')
        self._click_field('year')
        self._click_field('year_click')
        self._fill_field('user', form_fields['user'])
        self._fill_field('password', form_fields['password'])

        self._click_field('enter')
        time.sleep(6)
        self._click_field('daily_corona')
        time.sleep(3)
        self._select_box('confirm_1_box', 'confirm_1_check')
        self._select_box('confirm_2_box', 'confirm_2_check')
        if submit:
            time.sleep(3)

            # self._click_field('submit')
            try:
                self._driver.switch_to.alert.accept()
            except NoAlertPresentException:
                pass
            self._save_snapshot(form_fields['child_first_name'], 'submit_form')
