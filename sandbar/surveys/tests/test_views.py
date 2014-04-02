
import datetime

from django.contrib.gis.geos import Point
from django.test import TestCase

from ..models import Site, Survey
from ..views import SitesListView, _elevationM, _interpolateCalcs 

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
                         stage_discharge_coeff_a='231.2',
                         stage_discharge_coeff_b='0.0000003',
                         stage_discharge_coeff_c='-0.0023',
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
        
        self.survey1 = Survey.objects.create(site=self.site1, 
                                        survey_date=datetime.date(2013, 8, 30),
                                        survey_method='method1',
                                        uncrt_a_8000='231',
                                        uncrt_b_8000='999',
                                        discharge='389723.32')
        self.survey2 = Survey.objects.create(site=self.site1,
                                        survey_date=datetime.date(2013, 7, 1),
                                        survey_method='method1',
                                        uncrt_a_8000='90',
                                        uncrt_b_8000='99',
                                        discharge='38973.3')
        self.survey3 = Survey.objects.create(site=self.site1,
                                        survey_date=datetime.date(2013, 6, 1),
                                        survey_method='method1',
                                        uncrt_a_8000='100',
                                        uncrt_b_8000='998',
                                        discharge='3893.02')
        self.survey4 = Survey.objects.create(site=self.site2,
                                        survey_date=datetime.date(2013, 7, 1),
                                        survey_method='method1',
                                        uncrt_a_8000='2',
                                        uncrt_b_8000='1',
                                        discharge='383.0')
        
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
 
class ElevationMTestCase(TestCase):        
    def test_elevationM(self):
        Q = 23150
        a = 716.396358
        b = 0.0001658795122
        c = -0.000000001335143
        self.assertEqual(720.95200188184742, _elevationM(a,b,c,Q))
        
class InterpolateCalcsTestCase(TestCase):        
    def test_interpolateCalcs(self):
        xp = [833.66, 833.76]
        fp = [9585.930877, 9228.061652]
        Z = 833.7
        self.assertAlmostEqual(9442.783186999, _interpolateCalcs(xp, fp, Z))
                                        