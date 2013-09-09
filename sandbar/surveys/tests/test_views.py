
import datetime

from django.contrib.gis.geos import Point
from django.test import TestCase

from ..models import Site, Survey
from ..views import SitesListView

class SitesViewTestCase(TestCase):
    
    def setUp(self):
        self.site1 = Site(river_mile='1.0',
                         site_name='Name1',
                         deposit_type='a',
                         eddy_size='1.2',
                         exp_ratio_8000='2.3',
                         exp_ratio_45000='3.4',
                         stage_change='5.4',
                         sed_budget_reach='reach1',
                         campsite='NO',
                         geom=Point(-90.0, 35.0))
        self.site1.save()
        
        self.site2 = Site(river_mile='2.0',
                         site_name='Name2',
                         deposit_type='a',
                         eddy_size='1.2',
                         exp_ratio_8000='2.3',
                         exp_ratio_45000='3.4',
                         stage_change='5.4',
                         sed_budget_reach='reach1',
                         campsite='NO',
                         geom=Point(-90.0, 35.0))
        self.site2.save()
        
        self.site3 = Site(river_mile='3.0',
                         site_name='Name3',
                         deposit_type='a',
                         eddy_size='1.2',
                         exp_ratio_8000='2.3',
                         exp_ratio_45000='3.4',
                         stage_change='5.4',
                         sed_budget_reach='reach1',
                         campsite='NO',
                         geom=Point(-90.0, 35.0))
        self.site3.save()
        
        self.survey1 = Survey.objects.create(site=self.site1, 
                                        survey_date=datetime.date(2013, 8, 30),
                                        survey_method='method1')
        self.survey2 = Survey.objects.create(site=self.site1,
                                        survey_date=datetime.date(2013, 7, 1),
                                        survey_method='method1')
        self.survey3 = Survey.objects.create(site=self.site1,
                                        survey_date=datetime.date(2013, 6, 1),
                                        survey_method='method1')
        self.survey4 = Survey.objects.create(site=self.site2,
                                        survey_date=datetime.date(2013, 7, 1),
                                        survey_method='method1')
        
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
                                        