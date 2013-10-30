# -*- coding: utf-8 -*-
from sqlalchemy import Table, Column, String, Integer,ForeignKey, DateTime,Boolean
from db_engine import engine, Base

#################     CLASS     #####################
class Pagetitle(Base):
    __tablename__='pagetitles'
    id = Column('id',Integer,primary_key=True)
    rank=Column('rank', Integer)
    parent_id=Column('parent_id',Integer,ForeignKey('pagetitles.id'))
    mnemo = Column('mnemo',String)
    ptitle = Column('ptitle',String)
    added = Column('added', DateTime)
    in_use = Column('in_use',Boolean(True))
    def __init__(self,**kwargs):
        for k,v in kwargs.iteritems():
            setattr(self,k,v)
#####################################################
metadata = Base.metadata
metadata.create_all(engine)
