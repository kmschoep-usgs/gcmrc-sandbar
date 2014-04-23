from django.test import TestCase

from ..models import Site, AreaVolume
from factories import AreaVolumeCalcsFactory, SiteModelFactory



class TestAreaVolumeCalcsFactory(TestCase):
    
    
    def setUp(self):
        
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
        self.assertTrue(isinstance(av_calc, AreaVolume))
        
        
class TestSiteModelFactory(TestCase):
    
    
    def setUp(self):
        
        self.site_factory = SiteModelFactory(pk=970,
                                             river_mile = 60.98,
                                             river_side = 'L',
                                             site_name = 'Some site',
                                             gdaws_site_id = '5643890',
                                             gcmrc_site_id = '084L',
                                             deposit_type = 'U',
                                             eddy_size = 800,
                                             exp_ratio_8000 = 1.3,
                                             exp_ratio_45000 = 1.5,
                                             stage_change = 4.3,
                                             sed_budget_reach = 'Upper Marble Canyon',
                                             cur_stage_relation = 'y = mx + b',
                                             campsite = 'No',
                                             geom = None,
                                             stage_discharge_coeff_a = 1,
                                             stage_discharge_coeff_b = 2,
                                             stage_discharge_coeff_c = 3)
        
        
    def test_site_factory_instance(self):
        
        """
        Test that SiteModelFactory returns an instance of Site
        """
        
        site_factory_instance = self.site_factory
        self.assertTrue(isinstance(site_factory_instance, Site))
        
        