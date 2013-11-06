# -*- coding: utf-8 -*-
import os, sys

APP_NAME = 'DBdesk'
APP_VER = '0.1'
APP_TITLE = APP_NAME+' '+APP_VER
SQLITE_DB_DIR = os.environ['project_dir']+'/assets/db'
APP_DB = 'dbdesk.db'
SQLITE_APPDB_PATH = SQLITE_DB_DIR+'/'+APP_DB
SQLITE_DSCHEMA_FILE = 'schema.sql'
SQLITE_DSCHEMA_DIR = os.environ['project_dir']+'/assets/schema'
DATASCHEMA_PATH = SQLITE_DSCHEMA_DIR+'/'+SQLITE_DSCHEMA_FILE
USER_DIR_ROOT=os.environ['project_dir']+'/udirs'
DEMO_DIR_ROOT = os.environ['project_dir']+'/demos'
DEMO_DB_DIR = DEMO_DIR_ROOT+'/db'
ALLOWED_EXTENSIONS = set(['db',])
USERNAME='user'
PASSWORD='1111'
# max db size - 5Mbytes
MAX_CONTENT_LENGTH=5 * 1024 * 1024
