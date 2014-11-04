from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sandbar_project.local_settings import SCHEMA_USER, DB_PWD, DB_NAME
from .models import Sandbar
from .db_mappings import AreaVolumeCalcBase


def get_sep_reattch_data(sr_id):
    
    record = Sandbar.objects.get(id=sr_id)
    river_mile = record.river_mile
    return float(river_mile)


def convert_datetime_to_str(date_object, date_format='%Y-%m-%d'):
    
    """
    Convert a python date object to a string.
    """
    try:
        date_str = date_object.strftime(date_format)
    except AttributeError:
        date_str = None
    
    return date_str


def determine_if_sep_reatt_exists(site_id):
    result_list = get_sep_reatt_ids(site_id)
    if len(result_list) > 0:
        sr_exists = True
    else:
        sr_exists = False
    return sr_exists


def determine_site_survey_types(site_id):
    acdb = AlchemDB()
    ora_session = acdb.create_session()
    result = ora_session.query(AreaVolumeCalcBase.calc_type).filter(AreaVolumeCalcBase.site_id==site_id).distinct()
    result_list = []
    for record in result:
        result_list.append(record.calc_type)
    ora_session.close()
    return result_list


def get_sep_reatt_ids(site_id):
    qs = Sandbar.objects.filter(site_id=site_id)
    distinct_sandbar_results = [record.id for record in qs]
    return distinct_sandbar_results


class AlchemDB(object): 
    
    def __init__(self, schema=SCHEMA_USER, password=DB_PWD, db_name=DB_NAME):
        
        self.connect = 'oracle+cx_oracle://%s:%s@%s' % (schema, password, db_name)
        self.engine = create_engine(self.connect)
               
    def create_session(self):
        
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        session = Session()
        
        return session

    
def create_cx_oracle_auth_str(schema, pwd, db_name, ip_address=None):
    
    """
    Create the authentication string that 
    cx_Oracle will use to connect to the
    database
    """
    
    if ip_address:
        auth_str = '%s/%s@%s:1521/%s' % (schema, pwd, ip_address, db_name)
    else:
        auth_str = '%s/%s@%s' % (schema, pwd, db_name)
        
    return auth_str