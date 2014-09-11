from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Date

Base = declarative_base()


class SitesBase(Base):
    
    __tablename__ = 'SITES'
    
    campsite = Column(String)
    cur_stage_relation = Column(String)
    deposit_type = Column(String)
    eddy_size = Column(Integer)
    exp_ratio_45000 = Column(Numeric)
    exp_ratio_8000 = Column(Numeric)
    gcmrc_site_id = Column(String)
    gdaws_site_id = Column(String)
    id = Column(Integer, primary_key=True)
    river_mile = Column(Numeric)
    river_side = Column(String)
    sed_budget_reach = Column(String)
    site_name = Column(String)
    stage_change = Column(Numeric)
    stage_discharge_coeff_a = Column(Numeric)
    stage_discharge_coeff_b = Column(Numeric)
    stage_discharge_coeff_c = Column(Numeric)


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