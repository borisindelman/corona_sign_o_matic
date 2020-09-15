from collections import OrderedDict
import time
from time import strftime, gmtime

from fillers.form_filler_base import FormFillerBase


class KasumFormFiller(FormFillerBase):
    def __init__(self):
        self._url = r'https://docs.google.com/forms/d/e/1FAIpQLScROBXBxMJqrYz_kjU-JUrY6VMNMLCTaemWhYm_ucDUTsEFEw/viewform'
        super().__init__()

        self._xpaths = OrderedDict(
            {'date': r'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div/div[2]/div[1]/div/div[1]/input',
             'hebrew_child_first_name':  r'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input',
             'checked_temperature': r'//*[@id="i15"]/div[2]',
             'family_members': r'//*[@id="i23"]/div[2]',
             'symptoms': r'//*[@id="i31"]/div[2]',
             'temperature': r'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[1]/div/div[1]/input',
             'hebrew_parent_name': r'//*[@id="mG61Hd"]/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[1]/div/div[1]/input',
             'submit': r'//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span'
             })
        self.expected_snapshots = 2
        self.debug_snapshots = 1
        self.is_temperature_required = True


    def _fill_form(self, form_fields, submit=False):
        self._fill_field('date', strftime("%m/%d/%Y", gmtime()))
        self._fill_field('hebrew_child_first_name', form_fields['hebrew_child_first_name'])
        self._click_field('checked_temperature')
        self._click_field('family_members')
        self._click_field('symptoms')
        self._fill_field('temperature', str(form_fields['child_temperature']))
        self._fill_field('hebrew_parent_name', form_fields['hebrew_parent_name'])
        self._save_snapshot(form_fields['child_first_name'], 'filled_form')


        # submit
        if submit:
            self._click_field('submit')
            time.sleep(3)
            self._save_snapshot(form_fields['child_first_name'], 'submitted')
