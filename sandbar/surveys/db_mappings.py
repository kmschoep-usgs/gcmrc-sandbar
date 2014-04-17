from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Date

Base = declarative_base()

class AreaVolumeCalcBase(Base):
    
    __tablename__ = 'AREA_VOLUME_CALC'
    
    area_2d_amt = Column(Numeric)
    area_3d_amt = Column(Numeric)
    calc_date = Column(Date)
    calc_type = Column(String)
    id = Column(Integer, primary_key=True)
    next_plane_height = Column(Numeric)
    plane_height = Column(Numeric)
    prev_plane_height = Column(Numeric)
    sandbar_id = Column(Integer)
    site_id = Column(Integer)
    volume_amt = Column(Numeric)