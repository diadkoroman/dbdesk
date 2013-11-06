# -*- coding: utf-8 -*-
import os, re
from werkzeug import secure_filename
from dev.utils import randomizer as rnd

class DBdesk:
    def __init__(self,**kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)
        self.rnd = rnd

    # check for allowed database files
    def is_database_file(self,filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in self.config.get('ALLOWED_EXTENSIONS')

    # generate random name (key_length = integer from 1 to 124)
    def gen_rand_name(self,key_length):
        self.rand_name = self.rnd.random_name(key_length)

    # import database file
    def import_database_file(self,file):
        if file and self.is_database_file(file.filename):
            # create random dirname
            self.gen_rand_name(key_length=12)
            # create dirpath
            self.db_dir = '{0}/{1}/'.format(self.config.get('USER_DIR_ROOT'),self.rand_name)
            # create dir itself(if not exists)
            self.cr_dir(self.db_dir)
            # check file and save it
            filename = secure_filename(file.filename)
            self.db_path = os.path.join(self.db_dir, filename)
            file.save(self.db_path)
            return True
        else:
            return False


    # create dir with random name
    def cr_dir(self,path):
        if not os.path.isdir(path):
            os.mkdir(path)
            return True

