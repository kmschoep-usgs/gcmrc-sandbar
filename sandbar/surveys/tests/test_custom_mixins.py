from django.test import TestCase

from ..custom_mixins import CSVResponseMixin, JSONResponseMixin


class TestCSVMixin(TestCase):
    
    
    def setUp(self):
        
        self.dict_1 = {'Time': '2009/11/03', 'Area2d': 700}
        self.dict_2 = {'Time': '2009/11/04', 'Area2d': 800}
        self.fake_context = [self.dict_1, self.dict_2]
        self.keys = ['Time', 'Area2d']
        self.csv_mixin = CSVResponseMixin()
        
    
    def test_csv_mixin_status(self):
        
        """
        Test that the response comes back with a 200 status code
        """
        
        response = self.csv_mixin.render_to_csv_response(context=self.fake_context, data_keys=None)
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        
        
    def test_csv_mixin_content_type(self):
        
        """
        Test that the Content-Type is reported as csv
        """
        
        response = self.csv_mixin.render_to_csv_response(context=self.fake_context, data_keys=None)
        content_type = response['Content-Type']
        expected_content_type = 'text/csv'
        self.assertEqual(content_type, expected_content_type)
    
    def test_csv_mixin_content_format(self):
        
        """
        Test that the content is ostensibly csv
        """
        
        response = self.csv_mixin.render_to_csv_response(context=self.fake_context, data_keys=None)
        containing_text = 'Area2d,Time'
        self.assertContains(response, containing_text)
        
    
    def test_csv_mixin_key_ordering(self):
        
        """
        Test that the ordering of the csv can be adjusted
        """
        
        response = self.csv_mixin.render_to_csv_response(context=self.fake_context, data_keys=self.keys)
        containing_text = 'Time,Area2d'
        self.assertContains(response, containing_text)
        
        
class TestJSONMixin(TestCase):
    

    def setUp(self):
        
        self.dict_1 = {'Time': '2008/10/06', 'Area2d': 1200}
        self.dict_2 = {'Time': '2008/10/12', 'Area2d': 1600}
        self.fake_context = [self.dict_1, self.dict_2]
        self.json_mixin = JSONResponseMixin()   
    
    
    def test_json_mixin_status(self):
        
        """
        Test that the response comes back with a 200 status code
        """
        
        response = self.json_mixin.render_to_json_response(context=self.fake_context)
        status_code = response.status_code
        self.assertEqual(status_code, 200)
        
    
    def test_json_mixin_content_type(self):
        
        """
        Test that the response has a content type of json
        """
        
        response = self.json_mixin.render_to_json_response(context=self.fake_context)
        content_type = response['Content-Type']
        expected_content_type = 'application/json'
        self.assertEqual(content_type, expected_content_type)
        
    
    def test_json_mixin_content_format(self):
        
        """
        Test that the content is actually JSON
        """
        
        response = self.json_mixin.render_to_json_response(context=self.fake_context)
        expected_content = '[{"Area2d": 1200, "Time": "2008/10/06"}, {"Area2d": 1600, "Time": "2008/10/12"}]'
        self.assertContains(response, expected_content)
        
        
        
