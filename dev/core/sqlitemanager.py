# -*- coding: utf-8 -*-
import os, sqlite3
from configs.settings import DATASCHEMA_PATH
from contextlib import closing

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
