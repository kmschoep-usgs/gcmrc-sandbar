from sqlalchemy import create_engine, func
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
    dates = session.query(AreaVolumeCalcBase.calc_date).distinct(AreaVolumeCalcBase.calc_date).filter(func.lower(AreaVolumeCalcBase.calc_type)=='eddy').filter(AreaVolumeCalcBase.site_id=='38').order_by(AreaVolumeCalcBase.calc_date)
    for date in dates:
        print date
        d1 = session.query(AreaVolumeCalcBase.plane_height, AreaVolumeCalcBase.next_plane_height, AreaVolumeCalcBase.area_2d_amt).filter(AreaVolumeCalcBase.prev_plane_height!=0).order_by(AreaVolumeCalcBase.plane_height)
        d1_list = d1.all()
        print d1_list[0].plane_height
    session.close()
    