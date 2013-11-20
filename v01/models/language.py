# -*- coding: utf-8 -*-
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper
from db_engine import engine, Base

#languages_table = Table('languages',metadata,
#                 Column('id', Integer, primary_key=True),
#                 Column('nazva',String),
#                 Column('mnemo',String)
#)
#metadata.create_all(engine)
#####################################################


#####################################################
class Language(Base):
    __tablename__ = 'languages'
    id = Column('id', Integer, primary_key=True)
    nazva = Column('nazva',String)
    mnemo = Column('mnemo',String)


####################################################
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True)
    firstname = Column(String)
    surname = Column(String)
    nickname = Column(String)
    password = Column(String)
    def __init__(self,**kwargs):
        for k, v in kwargs.iteritems():
            setattr(self,k,v)

####################################################
metadata = Base.metadata        
metadata.create_all(engine)

#mapper(Language,languages_table)
