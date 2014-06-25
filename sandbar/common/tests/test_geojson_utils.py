import json
from django.test import SimpleTestCase

from ..utils.geojson_utils import create_geojson_point, create_geojson_feature, create_geojson_feature_collection


class TestGeoJSONPointCreation(SimpleTestCase):
    
    def setUp(self):
        
        self.latitude = -122.345
        self.longitude = 38.76
        
    def test_point_tuple_return(self):
        
        result = create_geojson_point(self.latitude, self.longitude)
        expected = (self.latitude, self.longitude)
        self.assertEqual(result, expected)
        
        
class TestGeoJSONFeatureCreation(SimpleTestCase):
    
    def setUp(self):
        
        self.point = (-122, 37)
        self.test_id = 8
        self.property = {'name': 'site_name', 'organization': 'USGS'}
        
    def test_feature_create_point(self):
        
        feature = create_geojson_feature(self.point)
        result = json.dumps(feature)
        expected = '{"geometry": {"type": "Point", "coordinates": [-122, 37]}, "type": "Feature", "id": null, "properties": {}}'
        self.assertEqual(result, expected)
        
    def test_feature_create_point_and_id(self):
        
        feature = create_geojson_feature(point=self.point, feature_id=self.test_id)
        result = json.dumps(feature)
        expected = '{"geometry": {"type": "Point", "coordinates": [-122, 37]}, "type": "Feature", "id": 8, "properties": {}}'
        self.assertEqual(result, expected)
        
    def test_feature_create_point_prop_id(self):
        
        feature = create_geojson_feature(point=self.point, properties=self.property, feature_id=self.test_id)
        result = json.dumps(feature)
        expected = '{"geometry": {"type": "Point", "coordinates": [-122, 37]}, "type": "Feature", "id": 8, "properties": {"organization": "USGS", "name": "site_name"}}'
        self.assertEqual(result, expected)
        
     
class TestGeoJSONFeatureCollectionCreation(SimpleTestCase):
    
    def setUp(self):
        
        self.point_1 = (-124, 34)
        self.point_2 = (-123, 33)
        self.feature_1 = create_geojson_feature(self.point_1)
        self.feature_2 = create_geojson_feature(self.point_2)
        self.feature_list = [
                             self.feature_1,
                             self.feature_2
                             ]
        
    def test_feature_collection_create(self):
        
        feature_collection = create_geojson_feature_collection(self.feature_list)
        result = json.dumps(feature_collection)
        expected = '{"type": "FeatureCollection", "features": [{"geometry": {"type": "Point", "coordinates": [-124, 34]}, "type": "Feature", "id": null, "properties": {}}, {"geometry": {"type": "Point", "coordinates": [-123, 33]}, "type": "Feature", "id": null, "properties": {}}]}' 
        self.assertEqual(result, expected)   