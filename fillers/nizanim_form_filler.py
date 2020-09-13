from collections import OrderedDict
import time
from time import strftime, gmtime

from fillers.form_filler_base import FormFillerBase


class NizanimFormFiller(FormFillerBase):
    def __init__(self):
        self._url = r'https://docs.google.com/forms/d/e/1FAIpQLSe5u16j3ibEnv86NHRcUbbZnJy9Z16HtMSDiV1dYnwDfTA2Gg/viewform'
        super().__init__(height_buffer=1700)

        self._xpaths = OrderedDict(
            {'email': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div[1]/div[2]/div[1]/div/div[1]/input',
             'date': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/input',
             'hebrew_child_first_name': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input',
             'hebrew_child_last_name': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input',
             'gan': '//*[@id="i22"]/div[3]/div',
             'child_id': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[1]/div/div[1]/input',
             'hebrew_parent_name': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[1]/div/div[1]/input',
             'phone_number': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[8]/div/div/div[2]/div/div[1]/div/div[1]/input',
             'below_38': '//*[@id="i57"]/div[2]',
             'cough': '//*[@id="i60"]/div[2]',
             'in_contact': '//*[@id="i63"]/div[2]',
             'remark': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[10]/div/div/div[2]/div/div[1]/div[2]/textarea',
             'submit': '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span'
             })
        self.expected_snapshots = 2
        self.debug_snapshots = 1

    def _fill_form(self, form_fields, submit=False):
        # time.sleep(10)
        self._fill_field('email', form_fields['email'])
        self._fill_field('date', strftime("%d/%m/%Y", gmtime()))
        self._fill_field('hebrew_child_first_name', form_fields['hebrew_child_first_name'])
        self._fill_field('hebrew_child_last_name', form_fields['hebrew_child_last_name'])
        self._click_field('gan')
        self._fill_field('child_id', form_fields['child_id'])
        self._fill_field('hebrew_parent_name', form_fields['hebrew_parent_name'])
        self._fill_field('phone_number', form_fields['phone_number'])
        self._click_field('below_38')
        self._click_field('cough')
        self._click_field('in_contact')
        self._fill_field('remark', 'אין')
        self._save_snapshot(form_fields['child_first_name'], 'filled_form')

        # submit
        if submit:
            self._click_field('submit')
            time.sleep(3)
            self._save_snapshot(form_fields['child_first_name'], 'submit_form')

