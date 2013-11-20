# -*- coding: utf-8 -*-
from sqlite3 import dbapi2 as sqlite
from configs.main import SQLITE_DB_FULLPATH
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dbc=create_engine('sqlite+pysqlite:///'+SQLITE_DB_FULLPATH,module=sqlite)
Base=declarative_base()
Session=sessionmaker(bind=dbc)
sess = Session()
metadata=Base.metadata
