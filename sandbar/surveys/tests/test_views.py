import datetime
import json
from unittest2 import skip
from django.contrib.gis.geos import Point
from django.test import TestCase, RequestFactory
from django.test.client import Client
from django.core.urlresolvers import reverse
from ..models import Site, AreaVolume
from ..views import SitesListView, _interpolateCalcs, AreaVolumeCalcsVw

from factories import AreaVolumeCalcsFactory, SiteModelFactory


class TestBasicSiteInfoJSON(TestCase):
    
    def setUp(self):
        
        self.site = Site()


class TestAreaVolumeCalcsVw(TestCase):
    
    def setUp(self):
        self.site1 = Site(pk='38',
                          river_mile='1.0',
                         site_name='Name1',
                         deposit_type='a',
                         eddy_size='1',
                         exp_ratio_8000='2.3',
                         exp_ratio_45000='3.4',
                         stage_change='5.4',
                         sed_budget_reach='reach1',
                         campsite='NO',
                         stage_discharge_coeff_a='833.110516580428',
                         stage_discharge_coeff_b='0.0001661346286',
                         stage_discharge_coeff_c='-0.000000001257274',
                         geom=Point(-90.0, 35.0))
        self.site1.save()
        self.site2 = Site(pk='18',
                          river_mile='1.0',
                         site_name='Name2',
                         deposit_type='a',
                         eddy_size='1',
                         exp_ratio_8000='2.3',
                         exp_ratio_45000='3.4',
                         stage_change='5.4',
                         sed_budget_reach='reach1',
                         campsite='NO',
                         stage_discharge_coeff_a='716.396358',
                         stage_discharge_coeff_b='0.0001658795122',
                         stage_discharge_coeff_c='-0.000000001335143',
                         geom=Point(-90.0, 35.0))
        self.site2.save()
        self.site3 = Site(pk='40',
                          river_mile='1.0',
                         site_name='Name3',
                         deposit_type='a',
                         eddy_size='1',
                         exp_ratio_8000='2.3',
                         exp_ratio_45000='3.4',
                         stage_change='5.4',
                         sed_budget_reach='reach1',
                         campsite='NO',
                         stage_discharge_coeff_a='850.396358',
                         stage_discharge_coeff_b='0.0001658795122',
                         stage_discharge_coeff_c='-0.000000001335143',
                         geom=Point(-90.0, 35.0))
        self.site3.save()
        self.av1 = AreaVolumeCalcsFactory(site_id = '38', calc_date = '1990-09-29', area_2d_amt = '11699.733846848', plane_height = '833.36', prev_plane_height = '0', next_plane_height = '833.46')                                                                                                                                    
        self.av2 = AreaVolumeCalcsFactory(site_id = '38', calc_date = '1990-09-29', area_2d_amt = '11690.851434872', plane_height = '833.46', prev_plane_height = '833.36', next_plane_height = '833.56')                                                                                                                               
        self.av3 = AreaVolumeCalcsFactory(site_id = '38', calc_date = '1990-09-29', area_2d_amt = '11481.042255916', plane_height = '833.56', prev_plane_height = '833.46', next_plane_height = '833.66')                                                                                                                               
        self.av4 = AreaVolumeCalcsFactory(site_id = '38', calc_date = '1990-09-29', area_2d_amt = '11148.121862074', plane_height = '833.66', prev_plane_height = '833.56', next_plane_height = '833.76')                                                                                                                               
        self.av5 = AreaVolumeCalcsFactory(site_id = '38', calc_date = '1990-09-29', area_2d_amt = '10790.252637538', plane_height = '833.76', prev_plane_height = '833.66', next_plane_height = '833.86')                                                                                                                               
        self.av6 = AreaVolumeCalcsFactory(site_id = '38', calc_date = '1990-09-29', area_2d_amt = '10466.534941901', plane_height = '833.86', prev_plane_height = '833.76', next_plane_height = '833.96')                                                                                                                               
        self.av7 = AreaVolumeCalcsFactory(site_id = '38', calc_date = '1990-09-29', area_2d_amt = '10176.014798972', plane_height = '833.96', prev_plane_height = '833.86', next_plane_height = '834.06')                                                                                                                               
        self.av8 = AreaVolumeCalcsFactory(site_id = '38', calc_date = '1990-09-29', area_2d_amt = '9841.843595994', plane_height = '834.06', prev_plane_height = '833.96', next_plane_height = '834.16')                                                                                                                                
        self.av9 = AreaVolumeCalcsFactory(site_id = '38', calc_date = '1990-09-29', area_2d_amt = '9485.851390867', plane_height = '834.16', prev_plane_height = '834.06', next_plane_height = '834.26')                                                                                                                                
        self.av10 = AreaVolumeCalcsFactory(site_id = '38', calc_date = '1990-09-29', area_2d_amt = '9120.851821026', plane_height = '834.26', prev_plane_height = '834.16', next_plane_height = '834.36')                                                                                                                                
        self.av11 = AreaVolumeCalcsFactory(site_id = '38', calc_date = '1990-09-29', area_2d_amt = '8741.933277075', plane_height = '834.36', prev_plane_height = '834.26', next_plane_height = '834.46')                                                                                                                                
        self.av12 = AreaVolumeCalcsFactory(site_id = '38', calc_date = '1990-09-29', area_2d_amt = '8349.142510525', plane_height = '834.46', prev_plane_height = '834.36', next_plane_height = '834.56')                                                                                                                                
        self.av13 = AreaVolumeCalcsFactory(site_id = '38', calc_date = '1990-09-29', area_2d_amt = '7941.451405398', plane_height = '834.56', prev_plane_height = '834.46', next_plane_height = '834.66')                                                                                                                                
        self.av14 = AreaVolumeCalcsFactory(site_id = '38', calc_date = '1990-09-29', area_2d_amt = '7426.137390517', plane_height = '834.66', prev_plane_height = '834.56', next_plane_height = '834.76')                                                                                                                                
        self.av15 = AreaVolumeCalcsFactory(site_id = '38', calc_date = '1990-09-29', area_2d_amt = '6939.768323272', plane_height = '834.76', prev_plane_height = '834.66', next_plane_height = '834.86')                                                                                                                                
        self.av16 = AreaVolumeCalcsFactory(site_id = '38', calc_date = '1990-09-29', area_2d_amt = '6562.76914809', plane_height = '834.86', prev_plane_height = '834.76', next_plane_height = '834.96')                                                                                                                                 
        self.av17 = AreaVolumeCalcsFactory(site_id = '38', calc_date = '1990-09-29', area_2d_amt = '6169.456558383', plane_height = '834.96', prev_plane_height = '834.86', next_plane_height = '835.06')                                                                                                                                
        self.av18 = AreaVolumeCalcsFactory(site_id = '38', calc_date = '1990-09-29', area_2d_amt = '5755.589387903', plane_height = '835.06', prev_plane_height = '834.96', next_plane_height = '835.16')    
        self.av19 = AreaVolumeCalcsFactory(site_id = '38', calc_date = '1990-09-29', area_2d_amt = '19.399386992', plane_height = '838.86', prev_plane_height = '838.76', next_plane_height = '838.96')                                                                                                                                      
        self.av20 = AreaVolumeCalcsFactory(site_id = '38', calc_date = '1990-09-29', area_2d_amt = '8.507177912', plane_height = '838.96', prev_plane_height = '838.86', next_plane_height = '839.06')                                                                                                                                   
        self.av21 = AreaVolumeCalcsFactory(site_id = '38', calc_date = '1990-09-29', area_2d_amt = '2.626584831', plane_height = '839.06', prev_plane_height = '838.96', next_plane_height = '839.16')                                                                                                                                   
        self.av22 = AreaVolumeCalcsFactory(site_id = '38', calc_date = '1990-09-29', area_2d_amt = '0', plane_height = '839.16', prev_plane_height = '839.06', next_plane_height = '839.16')
        
        self.av23 = AreaVolumeCalcsFactory(site_id = '18', calc_date = '1990-09-29', area_2d_amt = '11699.733846848', plane_height = '833.36', prev_plane_height = '0', next_plane_height = '833.46')                                                                                                                                    
        self.av24 = AreaVolumeCalcsFactory(site_id = '18', calc_date = '1990-09-29', area_2d_amt = '11690.851434872', plane_height = '833.46', prev_plane_height = '833.36', next_plane_height = '833.56')                                                                                                                               
        self.av25 = AreaVolumeCalcsFactory(site_id = '18', calc_date = '1990-09-29', area_2d_amt = '11481.042255916', plane_height = '833.56', prev_plane_height = '833.46', next_plane_height = '833.66')                                                                                                                               
        self.av26 = AreaVolumeCalcsFactory(site_id = '18', calc_date = '1990-09-29', area_2d_amt = '11148.121862074', plane_height = '833.66', prev_plane_height = '833.56', next_plane_height = '833.76')
        
        self.av27 = AreaVolumeCalcsFactory(site_id = '40', calc_date = '1990-09-29', area_2d_amt = '11699.733846848', plane_height = '833.36', prev_plane_height = '0', next_plane_height = '833.46')                                                                                                                                    
        self.av28 = AreaVolumeCalcsFactory(site_id = '40', calc_date = '1990-09-29', area_2d_amt = '11690.851434872', plane_height = '833.46', prev_plane_height = '833.36', next_plane_height = '833.56')                                                                                                                               
        self.av29 = AreaVolumeCalcsFactory(site_id = '40', calc_date = '1990-09-29', area_2d_amt = '11481.042255916', plane_height = '833.56', prev_plane_height = '833.46', next_plane_height = '833.66')                                                                                                                               
        self.av30 = AreaVolumeCalcsFactory(site_id = '40', calc_date = '1990-09-29', area_2d_amt = '11148.121862074', plane_height = '833.66', prev_plane_height = '833.56', next_plane_height = '833.76')
        self.ds_min = u'6500'
        self.ds_max = u'9000'
        self.test_view = AreaVolumeCalcsVw()      
        self.request_factory = RequestFactory()
    
    @skip('Necessary database function does not exist in test database.')    
    def test_area_vol_calcs_view_area_eddy(self):
        request = self.request_factory.get('/areavolume/', {'site_id': '38', 
                                                            'param_type': 'area2d', 
                                                            'ds_min': self.ds_min, 
                                                            'ds_max': self.ds_max, 
                                                            'calc_type': ['eddy']})
        response = self.test_view.get(request)
        expected_content_snippet_1 = 'Eddy Total'
        expected_content_snippet_2 = 1327
        self.assertContains(response, expected_content_snippet_1)
        self.assertContains(response, expected_content_snippet_2)


class SitesViewTestCase(TestCase):
    
    def setUp(self):
        self.site1 = Site(river_mile='1.0',
                         site_name='Name1',
                         deposit_type='a',
                         eddy_size='1',
                         exp_ratio_8000='2.3',
                         exp_ratio_45000='3.4',
                         stage_change='5.4',
                         sed_budget_reach='reach1',
                         campsite='NO',
                         stage_discharge_coeff_a='716.396358',
                         stage_discharge_coeff_b='0.0001658795122',
                         stage_discharge_coeff_c='-0.000000001335143',
                         geom=Point(-90.0, 35.0))
        self.site1.save()
        
        self.site2 = Site(river_mile='2.0',
                         site_name='Name2',
                         deposit_type='a',
                         eddy_size='1',
                         exp_ratio_8000='2.3',
                         exp_ratio_45000='3.4',
                         stage_change='5.4',
                         sed_budget_reach='reach1',
                         campsite='NO',
                         stage_discharge_coeff_a='931.23423',
                         stage_discharge_coeff_b='0.000003423',
                         stage_discharge_coeff_c='-0.12312',
                         geom=Point(-90.0, 35.0))
        self.site2.save()
        
        self.site3 = Site(river_mile='3.0',
                         site_name='Name3',
                         deposit_type='a',
                         eddy_size='1',
                         exp_ratio_8000='2.3',
                         exp_ratio_45000='3.4',
                         stage_change='5.4',
                         sed_budget_reach='reach1',
                         campsite='NO',
                         stage_discharge_coeff_a='593.23423',
                         stage_discharge_coeff_b='0.00083242',
                         stage_discharge_coeff_c='-0.000234324',
                         geom=Point(-90.0, 35.0))
        self.site3.save()
        
        self.avc1 = AreaVolume.objects.create(site=self.site1, 
                                        calc_date=datetime.date(2013, 8, 30),
                                        calc_type='eddy',
                                        volume_amt='231',
                                        area_2d_amt='999',
                                        area_3d_amt='389723.32',
                                        plane_height='1000',
                                        prev_plane_height='900',
                                        next_plane_height='1100')
        self.avc2 = AreaVolume.objects.create(site=self.site1,
                                        calc_date=datetime.date(2013, 7, 1),
                                        calc_type='eddy',
                                        volume_amt='231',
                                        area_2d_amt='999',
                                        area_3d_amt='389723.32',
                                        plane_height='1000',
                                        prev_plane_height='900',
                                        next_plane_height='1100')
        self.avc3 = AreaVolume.objects.create(site=self.site1,
                                        calc_date=datetime.date(2013, 6, 1),
                                        calc_type='eddy',
                                        volume_amt='231',
                                        area_2d_amt='999',
                                        area_3d_amt='389723.32',
                                        plane_height='1000',
                                        prev_plane_height='900',
                                        next_plane_height='1100')
        self.avc4 = AreaVolume.objects.create(site=self.site2,
                                        calc_date=datetime.date(2013, 7, 1),
                                        calc_type='eddy',
                                        volume_amt='231',
                                        area_2d_amt='999',
                                        area_3d_amt='389723.32',
                                        plane_height='1000',
                                        prev_plane_height='900',
                                        next_plane_height='1100')
        
        self.test_view = SitesListView()
       
    def test_get_query_set(self):
        result = self.test_view.get_queryset()
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]['site'], self.site1)
        self.assertEqual(result[0]['survey']['min_date'], datetime.date(2013, 6, 1))
        self.assertEqual(result[0]['survey']['max_date'], datetime.date(2013, 8, 30))
        
        self.assertEqual(result[1]['site'], self.site2)
        self.assertEqual(result[1]['survey']['min_date'], datetime.date(2013, 7, 1))
        self.assertEqual(result[1]['survey']['max_date'], datetime.date(2013, 7, 1))
        
        self.assertEqual(result[2]['site'], self.site3)
        self.assertIsNone(result[2]['survey']['min_date'])
        self.assertIsNone(result[2]['survey']['max_date']) 
      
    def test_elevationM(self):
        #result = self.test_view.get_queryset()
        ds_min = 3000
        ds_max = 23150
        self.assertAlmostEqual(716.906012, self.site1.elevationM(ds_min),5 )
        #self.assertAlmostEqual(720.952001, float(self.site1.elevationM(ds_min, ds_max)[1]),5 )
        
        
class InterpolateCalcsTestCase(TestCase):        
    def test_in_range(self):
        xp = [833.66, 833.76]
        fp = [9585.930877, 9228.061652]
        Z = 833.7
        result = _interpolateCalcs(xp, fp, Z)
        self.assertAlmostEqual(9442.783186999, result)
    
    def test_in_range2(self):
        xp = [834.160000000, 834.260000000]
        fp = [9485.851390867, 9120.851821026]
        Z = 834.243511493
        result = _interpolateCalcs(xp, fp, Z)
        self.assertAlmostEqual(9181.0348006, result)
        
    def test_min_val(self):
        xp = [833.66, 833.76]
        fp = [9585.930877, 9228.061652]
        Z = 833.66
        result = _interpolateCalcs(xp, fp, Z)
        self.assertAlmostEqual(9585.930877, result)
        
    def test_max_val(self):
        xp = [833.66, 833.76]
        fp = [9585.930877, 9228.061652]
        Z = 833.76
        result = _interpolateCalcs(xp, fp, Z)
        self.assertAlmostEqual(9228.061652, result)


class SiteDetailViewTestCase(TestCase):
    
    
    def setUp(self):
        
        self.c = Client()
        self.site_230 = SiteModelFactory(pk=230,
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
        
    @skip('Causing decimal problems on Python 2.6... CI uses 2.6')
    def test_return_site_id_in_context(self):
        
        """
        Test that the site id is returned correctly in the context
        """
        
        test_pk = '230'
        response = self.c.get(reverse('surveys-site', kwargs={'pk': test_pk}))
        context = response.context[1]
        site = context['site']
        self.assertEqual(str(site.id), test_pk)

        
class TestSandBarSitesGeoJSON(TestCase):
    
    def setUp(self):
        self.site1 = Site(river_mile='16.0',
                         site_name='Fake Site 1',
                         deposit_type='a',
                         eddy_size='3',
                         exp_ratio_8000='2.3',
                         exp_ratio_45000='3.4',
                         stage_change='5.4',
                         sed_budget_reach='reach1',
                         campsite='NO',
                         stage_discharge_coeff_a='717.396358',
                         stage_discharge_coeff_b='0.0001638795122',
                         stage_discharge_coeff_c='-0.000000001435143',
                         geom=Point(-128.6, 84.9))
        self.site1.save() 
        self.site2 = Site(river_mile='19.0',
                         site_name='Fake Site 2',
                         deposit_type='a',
                         eddy_size='1',
                         exp_ratio_8000='2.3',
                         exp_ratio_45000='3.4',
                         stage_change='5.4',
                         sed_budget_reach='reach1',
                         campsite='NO',
                         stage_discharge_coeff_a='757.392458',
                         stage_discharge_coeff_b='0.0001038795122',
                         stage_discharge_coeff_c='-0.000000001432133',
                         geom=Point(-130.6, 89.1))
        self.site2.save()
        self.c = Client()
        
    def test_view_response_status(self):
        
        """
        Test that the view responds
        """
        
        response = self.c.get(reverse('gjson_sites'))
        status_code = response.status_code
        expected = 200
        self.assertEqual(status_code, expected)
        
    def test_response_content(self):
        
        """
        Verify that the expected GeoJSON attributes are present
        """
        
        response = self.c.get(reverse('gjson_sites'))
        self.assertContains(response, 'FeatureCollection')
        self.assertContains(response, 'Feature')
        self.assertContains(response, 'Point')
        
    def test_response_length(self):
        
        """
        Verify that two features are returned.
        These are the same two features that 
        were setup.
        """
        
        response = self.c.get(reverse('gjson_sites'))
        data = json.loads(response.content)
        data_features = data[u'features']
        self.assertEqual(len(data_features), 2)
        
    def test_point_coordinates(self):
        
        """
        Verify that the coordinates for the points
        are created correctly.
        """
        
        response = self.c.get(reverse('gjson_sites'))
        expected_point_text = '"geometry": {"type": "Point", "coordinates": [-128'
        self.assertContains(response, expected_point_text)