# -*- coding: utf-8 -*-
import sqlite3
from configs.settings import DATASCHEMA_PATH
from contextlib import closing

### CLASS DEFINITION ###
class SQLiteManager:
    q_startswith=('insert','update','delete')
    def __init__(self,db_path):
        self.db_path = db_path
    # sqlite file connection
    def connect_db(self):
        if sqlite3:
            return sqlite3.connect(self.db_path)

    # get database
    def get_db(self):
        db = self.connect_db()
        db.row_factory = sqlite3.Row
        return db

    #
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

    # init database
    def init_db(self):
        with closing(self.connect_db()) as db:
            with open(DATASCHEMA_PATH) as f:
                db.cursor().executescript(f.read())
                db.commit()
