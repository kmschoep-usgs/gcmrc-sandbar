from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class QueryDB(object):
    
    
    def __init__(self, schema, password, db_name):
        
        self.connect = 'oracle+cx_oracle://%s:%s@%s' % (schema, password, db_name)
        self.engine = create_engine(self.connect)
        
        
    def create_session(self):
        
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        session = Session()
        
        return session
        
        
if __name__ == '__main__':
    
    from sandbar_project.local_settings import SCHEMA_USER, DB_PWD, DB_DESC
    from db_mappings import AreaVolumeCalcBase
    
    q = QueryDB(SCHEMA_USER, DB_PWD, DB_DESC)
    session = q.create_session()
    query_results = session.query(AreaVolumeCalcBase.calc_date).distinct(AreaVolumeCalcBase.calc_date)
    for instance in query_results:
        print instance.calc_date
    session.close()
    