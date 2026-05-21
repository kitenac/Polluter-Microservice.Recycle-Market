from sqlalchemy import Column, ForeignKey, Integer, CHAR, VARCHAR, TIMESTAMP, Interval, NUMERIC
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship  # high level data access for related tables
import uuid
import inspect
import datetime


Base = declarative_base()

class Models:
    '''class-container for easy access to all existing model-classes via get_all_DB_models() method '''
    
    @staticmethod
    def get_all_DB_models(): 
        '''
        get all DB`s tables` models:
            i.e all nested (inner) classes + that`re related to DB table
        '''
        return [ attr for attr in Models.__dict__.values() 
                 if inspect.isclass(attr) and hasattr(attr, '__tablename__') ]

    class CommonModel(Base):
        __abstract__ = True   # Class will not create table - just tamplate for other tables
        id = Column(CHAR(36), default=uuid.uuid4, primary_key=True)
        created_at = Column(TIMESTAMP, default=datetime.datetime.now())       # func - use some sql-function from database   
        updated_at = Column(TIMESTAMP, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    class WasteCategory(CommonModel):
        __tablename__ = 'WasteCategory'
        id = None # exclude common PK - here it`s different PK - category
        
        category = Column(VARCHAR(32), primary_key=True, nullable=False) # uniqness off waste competly relys on it`s name (unlike organizations that may have common names)
        time_to_recycle = Column(Interval, nullable=False)               # usage:  datetime.timedelta(hours=152, minutes=21) | how much it takes to recycle this waste
        
        def __repr__(self):
            return self.category

    class Polluter_OO(CommonModel):
        __tablename__ = 'Polluter_OO'
        name  = Column(VARCHAR(64), nullable=False)
        
        # 2D-geo with 6 digets before and after comma 
        # - 12 digets in total, where 6 are for precision
        x_geo = Column(NUMERIC(12,6, asdecimal=False), nullable=False)  # asdecimal=False - permits floats as value without casting to Decimal type
        y_geo = Column(NUMERIC(12,6, asdecimal=False), nullable=False)

        polluter_waste = relationship('PolluterWaste', back_populates='polluter')
        
        def __repr__(self):
            return self.name

    class PolluterWaste(CommonModel):
        __tablename__ = 'PolluterWaste'
        amount      = Column(Integer, default=0)
        category    = Column(VARCHAR(32), ForeignKey('WasteCategory.category'))           # here I think no need to CASCADE deletion - let info about category present after category was removed
        polluter_id = Column(CHAR(36), ForeignKey('Polluter_OO.id', ondelete='CASCADE'))  # !!! 'CASCADE' deletion when Polluter (parent) is gone

        # define relations. also needed to correct svg generation of Tables relations
        polluter = relationship('Polluter_OO', back_populates='polluter_waste')
        waste    = relationship('WasteCategory')

        def __repr__(self):
            return f'{self.category}-{self.polluter_id}'
        
    class TestCI3(CommonModel):
        __tablename__ = 'TestCI'
        kek = Column(CHAR(32), default=67)