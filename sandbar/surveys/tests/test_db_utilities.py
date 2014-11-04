from datetime import date
from django.test import TestCase
from unittest2 import skip
from .factories import SandbarModelFactory, SiteModelFactory
from ..db_utilities import convert_datetime_to_str, get_sep_reatt_ids, determine_if_sep_reatt_exists

class TestDateTimeConversions(TestCase):
    
    def setUp(self):
        
        self.date_obj = date(2014, 7, 15)
        self.date_str = '2014-07-15'
        
    def test_convert_datetime_to_str(self):
        
        date_str = convert_datetime_to_str(self.date_obj)
        expected_str = self.date_str
        self.assertEqual(date_str, expected_str)
        

class TestDeterminationIfSeparationReattachmentExists(TestCase):
    
    def setUp(self):
        self.site_id = 230
        self.site_230 = SiteModelFactory(pk=self.site_id,
                                         river_mile=60.98,
                                         river_side='L',
                                         site_name='Some site',
                                         gdaws_site_id='0983242',
                                         gcmrc_site_id='084L',
                                         deposit_type='U',
                                         eddy_size=800,
                                         exp_ratio_8000=1.3,
                                         exp_ratio_45000=1.5,
                                         stage_change=4.3,
                                         sed_budget_reach='Upper Marble Canyon',
                                         cur_stage_relation='y = mx + b',
                                         campsite='No',
                                         geom=None,
                                         stage_discharge_coeff_a=1,
                                         stage_discharge_coeff_b=2,
                                         stage_discharge_coeff_c=3)
        self.sr1 = SandbarModelFactory(site=self.site_230, sandbar_name='sep')
        self.sr2 = SandbarModelFactory(site=self.site_230, sandbar_name='reatt')
        self.site_id_no_data = 700
        
        def test_sr_exists(self):
            
            result = determine_if_sep_reatt_exists(self.site_id)
            self.assertTrue(result)
            
        def test_sr_does_not_exist(self):
            
            result = determine_if_sep_reatt_exists(self.site_id_no_data)
            self.assertFalse(result)
            
        
class TestGetSeparationReattachment(TestCase):
    
    def setUp(self):
        self.site_id = 230
        self.site_230 = SiteModelFactory(pk=self.site_id,
                                         river_mile=60.98,
                                         river_side='L',
                                         site_name='Some site',
                                         gdaws_site_id='0983242',
                                         gcmrc_site_id='084L',
                                         deposit_type='U',
                                         eddy_size=800,
                                         exp_ratio_8000=1.3,
                                         exp_ratio_45000=1.5,
                                         stage_change=4.3,
                                         sed_budget_reach='Upper Marble Canyon',
                                         cur_stage_relation='y = mx + b',
                                         campsite='No',
                                         geom=None,
                                         stage_discharge_coeff_a=1,
                                         stage_discharge_coeff_b=2,
                                         stage_discharge_coeff_c=3)
        self.sr1 = SandbarModelFactory(site=self.site_230, sandbar_name='sep')
        self.sr2 = SandbarModelFactory(site=self.site_230, sandbar_name='reatt')
        self.site_id_no_data = 700
        
    @skip('Causing decimal problems on Python 2.6... CI uses 2.6')     
    def test_get_sep_reatt_ids(self):
        
        result_list = get_sep_reatt_ids(self.site_id)
        expected_len = 2
        self.assertEqual(len(result_list), expected_len)
        
    @skip('Causing decimal problems on Python 2.6... CI uses 2.6')   
    def test_get_set_reatt_ids_no_data(self):
        
        result_list = get_sep_reatt_ids(self.site_id_no_data)
        expected_len = 0
        self.assertEqual(len(result_list), expected_len)