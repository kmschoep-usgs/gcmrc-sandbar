from django.test import TestCase

from ..models import Site, AreaVolume, Sandbar
from factories import AreaVolumeCalcsFactory, SiteModelFactory, SandbarModelFactory


class TestSandbarModelFactory(TestCase):
    
    def setUp(self):
        
        self.sandbar = Sandbar
        self.site_id = 230
        self.site_230 = SiteModelFactory(pk=self.site_id,
                                         river_mile='60.98',
                                         river_side='L',
                                         site_name='Some site',
                                         gdaws_site_id='0983242',
                                         gcmrc_site_id='084L',
                                         deposit_type='U',
                                         eddy_size=800,
                                         exp_ratio_8000='1.3',
                                         exp_ratio_45000='1.5',
                                         stage_change='4.3',
                                         sed_budget_reach='Upper Marble Canyon',
                                         cur_stage_relation='y = mx + b',
                                         campsite='No',
                                         geom=None,
                                         stage_discharge_coeff_a='1',
                                         stage_discharge_coeff_b='2',
                                         stage_discharge_coeff_c='3')
        self.sr1 = SandbarModelFactory(site=self.site_230, sandbar_name='sep')
        
    def test_sandbar_instance(self):
        
        self.sandbar_instance = self.sr1
        self.assertTrue(isinstance(self.sandbar_instance, self.sandbar))    
        

class TestAreaVolumeCalcsFactory(TestCase):
    
    
    def setUp(self):
        
        self.av = AreaVolume
        self.av_calc_model_instance = AreaVolumeCalcsFactory(site_id = '678', 
                                                             calc_date = '1990-09-29', 
                                                             area_2d_amt = '0', 
                                                             plane_height = '839.16', 
                                                             prev_plane_height = '839.06', 
                                                             next_plane_height = '839.16')
    
    
    def test_area_volume_calc_factory_instance(self):
        
        """
        Test that AreaVolumeCalcsFactory returns an instance of AreaVolume
        """
            
        av_calc = self.av_calc_model_instance
        self.assertTrue(isinstance(av_calc, self.av))
        
        
class TestSiteModelFactory(TestCase):
    
    
    def setUp(self):
        
        self.site = Site
        self.site_factory = SiteModelFactory(pk='970',
                                             river_mile = '60.98',
                                             river_side = 'L',
                                             site_name = 'Some site',
                                             gdaws_site_id = '5643890',
                                             gcmrc_site_id = '084L',
                                             deposit_type = 'U',
                                             eddy_size = '800',
                                             exp_ratio_8000 = '1.3',
                                             exp_ratio_45000 = '1.5',
                                             stage_change = '4.3',
                                             sed_budget_reach = 'Upper Marble Canyon',
                                             cur_stage_relation = 'y = mx + b',
                                             campsite = 'No',
                                             geom = None,
                                             stage_discharge_coeff_a = '1',
                                             stage_discharge_coeff_b = '2',
                                             stage_discharge_coeff_c = '3'
                                             )
        
    def test_site_factory_instance(self):
        
        """
        Test that SiteModelFactory returns an instance of Site
        """
        
        site_factory_instance = self.site_factory
        self.assertTrue(isinstance(site_factory_instance, self.site))
        
        