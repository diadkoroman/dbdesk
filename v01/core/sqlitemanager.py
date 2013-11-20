# -*- coding: utf-8 -*-
import os, sqlite3
from v01.configs.settings import DATASCHEMA_PATH,DEMO_DB_SCRIPT 
from contextlib import closing

from sqlite3 import dbapi2 as sqlite
from sqlalchemy import create_engine, MetaData,Table, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

### CLASS DEFINITION ###
class SQLiteManager:
    q_startswith=('insert','update','delete')
    
    def __init__(self,dbpath):
        self.dbpath = dbpath
        self.init_db()
        
    def connect_db(self):
        if sqlite3:
            return sqlite3.connect(self.dbpath)

    # init database
    def init_db(self):
        with closing(self.connect_db()) as db:
            with open(DATASCHEMA_PATH) as f:
                db.cursor().executescript(f.read())
                db.commit()
            
    # get database
    def get_db(self):
        db = self.connect_db()
        db.row_factory = sqlite3.Row
        return db

    def q(self,query,args=(),one = False):
        db = self.get_db()
        try:
            res = db.cursor().execute(query,args).fetchall()
            if query.startswith(self.q_startswith):
                db.commit()
                return True
            else:
                return (res[0] if res else None) if one else res
        except:
            return False

    # get database name
    def get_dbname(self):
        dbfull = self.q("pragma database_list",one=True)
        return os.path.basename(dbfull[2])

    # get columns
    def get_columns(self,tablename):
        columns = self.q("pragma table_info({0})".format(tablename))
        return columns
        
    # get all table rows
    def get_table_content(self,tablename):
        return self.q("select * from {0}".format(tablename))

    # get tables listing
    def get_tables_list(self):
        items=self.q("select name from sqlite_master where type='table' order by name")
        return [item[0] for item in items]

    # get pk column
    def get_pk(self,columns):
        for c in columns:
            if c['pk'] == 1:
                return c['name']

############ SQLITE MANAGER ver. 2 ###################
class SQLiteManager2:
    
    q_startswith=('insert','update','delete')
    
    
    def __init__(self,dbpath):
        self.dbpath = dbpath
        self.dbc=create_engine('sqlite+pysqlite:///{0}'.format(self.dbpath),module=sqlite)
        self.Base=declarative_base()
        self.Session=sessionmaker(bind=self.dbc)
        self.sess = self.Session()
        self.metadata=self.Base.metadata
        self._get_tables_list()
        self._create_tables()
        self.tables = self.metadata.tables.keys()

    # create_demo_db
    def create_demodb(self):
        try:
            for q in DEMO_DB_SCRIPT:
                self.dbc.execute(q)
            self._get_tables_list()
            self._create_tables()
            self.tables = self.metadata.tables.keys()
        except:
            raise Exception('Script hasn`t been executed')

    # get database name
    def get_dbname(self):
        dbq = self.dbc.execute("pragma database_list")
        dbfull = dbq.first()
        return os.path.basename(dbfull[2])

    def _get_tables_list(self):
        self.tnames=[ex[0] for ex in self.dbc.execute("select name from sqlite_master where type='table' order by name")]

    def get_columns_list(self,tablename):
        self.columns=self.metadata.tables[tablename].c
        return self.columns
        #return self.dbc.execute("pragma table_info({0})".format(tablename))

    def get_table_content(self,tablename):
        return self.sess.query(self.dbtables[tablename]).all()

    def _parse_column(self,column):
        col = str(column['name'])
        if int(column['pk']) == 1:
            col = Column(col,Integer,primary_key=True)
        else:
            col = Column(col,Integer)
        return col


    def _create_tables(self):
        self.columns=''
        self.dbtables={}
        for tablename in self.tnames:
            tablename=str(tablename)
            self.dbtables[tablename] = Table(tablename,self.metadata,autoload=True,autoload_with=self.dbc)
        self.metadata.create_all(self.dbc)
        
