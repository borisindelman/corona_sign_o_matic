from collections import OrderedDict
import time
from time import strftime, gmtime

from fillers.form_filler_base import FormFillerBase


class ReallyFormFiller(FormFillerBase):
    def __init__(self):
        self._url = r'https://forms.office.com/Pages/ResponsePage.aspx?id=q-zudymq8EqWdq6fOE-ZLVl3deFdlz1Ntret4bJZePRUOE1aN1pJRUpFQTZUTkdQMDZQTUlMODlRSyQlQCN0PWcu'
        super().__init__(height_buffer=1500)

        self._xpaths_heb = OrderedDict(
            {
             'hebrew_child_last_name':  r'//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div/div[2]/div/div/input',
             'hebrew_child_first_name': r'//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div/div[2]/div/div/input',
                'child_id': r'//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[3]/div/div[2]/div/div/input',
                'hebrew_parent_name': r'//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[4]/div/div[2]/div/div/input',
                'phone_number': r'//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[5]/div/div[2]/div/div/input',
                'approval': r'//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[6]/div/div[2]/div/div/div/label/input',
                'date': r'//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[7]/div/div[2]/div/div/div/input[1]',
                'submit': r'//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[3]/div[1]/button/div'
             })
        self._xpaths_en_il = OrderedDict(
            {
             'hebrew_child_last_name':  r'//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[3]/div/div/div/input',
             'hebrew_child_first_name': r'//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[2]/div[2]/div[3]/div/div/div/input',
                'child_id': r'//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[3]/div[2]/div[3]/div/div/div/input',
                'hebrew_parent_name': r'//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div/div/input',
                'phone_number': r'//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[5]/div/div[2]/div/div/input',
                'approval': r'//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[6]/div/div[2]/div/div/div/label/input',
                'date': r'//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[2]/div[7]/div/div[2]/div/div/div/input[1]',
                'submit': r'//*[@id="form-container"]/div/div/div/div/div[1]/div[2]/div[3]/div[1]/button/div'
             })
        self._xpaths_en_us = self._xpaths_heb

        self._xpaths_en_US = self._xpaths_en_il
        self.expected_snapshots = 2
        self.debug_snapshots = 1

    def _fill_form(self, form_fields, submit=False):
        if r'lang="he"' in self._driver.page_source:
            self._xpaths = self._xpaths_heb
        elif r'lang="en-IL"' in self._driver.page_source:
            self._xpaths = self._xpaths_en_il
        elif r'lang="en-us"' in self._driver.page_source:
            self._xpaths = self._xpaths_en_us
        elif r'lang="en-US"' in self._driver.page_source:
            self._xpaths = self._xpaths_en_US
        # time.sleep(10)
        self._fill_field('hebrew_child_last_name', form_fields['hebrew_child_last_name'])
        self._fill_field('hebrew_child_first_name', form_fields['hebrew_child_first_name'])
        self._fill_field('child_id', form_fields['child_id'])
        self._fill_field('hebrew_parent_name', form_fields['hebrew_parent_name'])
        self._fill_field('phone_number', form_fields['phone_number'])
        self._click_field('approval')
        self._fill_field('date', strftime("%m/%d/%Y", gmtime()))
        self._save_snapshot(form_fields['child_first_name'], 'filled_form')

        # submit
        if submit:
            self._click_field('submit')
            time.sleep(3)
            self._save_snapshot(form_fields['child_first_name'], 'submit_form')

