from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import cx_Oracle
from sandbar_project.local_settings import SCHEMA_USER, DB_PWD, DB_NAME
from .models import Sandbar
from .db_mappings import AreaVolumeCalcBase


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


class OracleConnection(object):
    
    def __init__(self, schema=SCHEMA_USER, pwd=DB_PWD, db_name=DB_NAME):
        
        self.oa = create_cx_oracle_auth_str(schema, pwd, db_name, ip_address=None)
        
    def run_oracle_query(self, sql_query, close_connection=True):
        
        """
        Execute a SQL query and returns the results
        as a list of dictionaries
        """
        
        ora = cx_Oracle.connect(self.oa)
        cursor = ora.cursor()
        cursor.execute(sql_query)
        columns = [desc[0] for desc in cursor.description]
        record_list_dic = [dict(zip(columns, record)) for record in cursor]
        if close_connection:
            ora.close()
        
        return (ora, record_list_dic)
            
    def execute_dml(self, dml_list, close_connection=True):
        
        """
        Execute a list of SQL commands and report the failures with errors.
        """
        
        failed_list = []
        
        ora = cx_Oracle.connect(self.oa)
        cursor = ora.cursor()
        sql_statment_count = len(dml_list)
        for sql_statement in dml_list:
            try:
                cursor.execute(sql_statement)
            except(cx_Oracle.Error), exc:
                failed_dictionary = {}
                error, = exc.args
                failed_dictionary['error'] = error.message
                failed_dictionary['statement'] = sql_statement
                failed_list.append(failed_dictionary) 
                continue
        cursor.close()
        ora.commit()
        if close_connection:
            ora.close()
            
        results = {'total_count': sql_statment_count,
                   'failed_count': len(failed_list),
                   'failed_list': failed_list}    
            
        return results

    
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