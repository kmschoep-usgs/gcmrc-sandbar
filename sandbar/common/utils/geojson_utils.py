from geojson import Point, Feature, FeatureCollection

def create_geojson_point(latitude_value, longitude_value):
    
    point_tuple = (latitude_value, longitude_value)
    
    return point_tuple

def create_geojson_feature(point, properties={}, feature_id=None):
    """
    point is a (lon, lat) tuple,
    properties is a dictionary (e.g. {'country': 'Spain})
    """
    
    gj_point = Point(point)
    gj_feature = Feature(geometry=gj_point, properties=properties, id=feature_id)
    
    return gj_feature


def create_geojson_feature_collection(feature_list):
     
    gs_feature_collection = FeatureCollection(feature_list)
    
    return gs_feature_collection