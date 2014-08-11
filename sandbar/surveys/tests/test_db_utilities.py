from datetime import date
from django.test import TestCase

from ..db_utilities import convert_datetime_to_str

class TestDateTimeConversions(TestCase):
    
    def setUp(self):
        
        self.date_obj = date(2014, 7, 15)
        self.date_str = '2014-07-15'
        
    def test_convert_datetime_to_str(self):
        
        date_str = convert_datetime_to_str(self.date_obj)
        expected_str = self.date_str
        self.assertEqual(date_str, expected_str)