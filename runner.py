# -*- coding: utf-8 -*-
import os, re
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response
from forms.sqlterm import SQLTerminal as Terminal
from forms.importdb import ImportDBForm as IDBForm
from forms.ext.df import AddEntryForm
from utils import randomizer, sqlterminal
from wtforms import validators
from core.sqlitemanager import SQLiteManager
from core.dbdesk import DBdesk
app = Flask(__name__)
app.debug = True
app.config.from_object('configs.settings')

#-----------init block---------------

sqlm = SQLiteManager(app.config.get('SQLITE_APPDB_PATH'))
sqlm.init_db()
dbdesk = DBdesk(config = app.config)

#--------- routing|views ------------

@app.route('/', methods=['GET','POST'])
def home_view():
        return redirect(url_for('sqlite_view'))


@app.route('/SQLite/', methods=['GET','POST'])
def sqlite_view():
    sitelogo = app.config.get('APP_TITLE')
    terminal = Terminal(request.form)
    idb_form = IDBForm(request.form)
    ########### РОБОТА ІМПОРТУ БД ###########
    if request.method == 'POST' and idb_form.validate():
        file = request.files['db_file']
        if dbdesk.import_database_file(file):
            session['db_dir'] = dbdesk.db_dir
            session['db_path'] = dbdesk.db_path

    ############## якщо є шлях до бд - підключаємо термінал ##################
    if session.get('db_path'):
        sqlm.db_path = session['db_path']
        try:
            ########## РОБОТА SQL ТЕРМІНАЛУ #############
            if request.method == 'POST' and terminal.validate():
                trm_data = terminal.q(sqlm)
                if not trm_data:
                    flash('Wrong request')
            #########################################
            #tables = sqlm.q("select name from sqlite_master where type='table' order by name")
            tables =[item[0] for item in sqlm.q("select name from sqlite_master where type='table' order by name")]
            dbname = sqlm.q("pragma database_list",one=True)
            return render_template('dbman.html',
                    dbname=os.path.basename(dbname[2]),
                    tables=tables,
                    logo = sitelogo,
                    sqlt_form=terminal,
                    db_path=session.get('db_path') if session.get('db_path') else False)
        except:
            return 'path enabled but not managed'
    else:
        return render_template('import_db.html',logo = sitelogo,idb_form=idb_form)
        #########################################





@app.route('/SQLite/tables/', methods=['GET','POST'])
@app.route('/SQLite/tables/<table>/', methods=['GET','POST'])
def viewtable_view(table = None, option = None):
    sitelogo = app.config.get('APP_TITLE')
    terminal = Terminal(request.form)
    trm_data = None
    ########## SQL TERMINAL WORK #############
    if request.method == 'POST' and terminal.validate():
        trm_data = terminal.q(sqlm)
        if not trm_data:
            flash('Wrong request')
        elif isinstance(trm_data,(bool,)):
            flash('No such data')
    #########################################
    if session.get('db_path'):
        sqlm.db_path = session['db_path']
        tables =[item[0] for item in sqlm.q("select name from sqlite_master where type='table' order by name")]
        dbname = sqlm.q("pragma database_list",one=True)
        if table:
            columns = sqlm.q("pragma table_info({0})".format(table))
            table_content = sqlm.q("select * from {0}".format(table))
            table_rows = len(table_content)
            if trm_data and not isinstance(trm_data,(bool,)):
                table_content = trm_data

            return render_template('components/table_content.html',
                    dbname=os.path.basename(dbname[2]),
                    tbname=table,
                    tables=tables,
                    columns=columns,
                    table_content=table_content,
                    table_rows=table_rows,
                    logo = sitelogo,
                    sqlt_form=terminal,
                    db_path=session.get('db_path') if session.get('db_path') else False)
        else:
            return redirect(url_for('home_view'))

    else:
        return redirect(url_for('home_view'))


@app.route('/SQLite/tables/<table>/<option>/', methods=['GET','POST'])
def add_entry_view(table = None, option=None):

    if session.get('db_path'):
        sitelogo = app.config.get('APP_TITLE')
        terminal = Terminal(request.form)
        trm_data = None
        options=('add','delete')
        #tables list
        tables = [item[0] for item in sqlm.q("select name from sqlite_master where type='table' order by name")]
        if table in tables:
            ########## SQL TERMINAL WORK #############
            if request.method == 'POST' and terminal.validate():
                trm_data = terminal.q(sqlm)
                if not trm_data:
                    flash('Wrong request')
            #########################################
            table_content = sqlm.q("select * from {0}".format(table))
            columns = sqlm.q("pragma table_info({0})".format(table))
            #table_rows = len(table_content)
            if trm_data:
                table_content = trm_data
            if option in options:
                if option == 'add':
                   # create form backend
                   af = AddEntryForm(formdata=request.form,table=table,columns=columns)
                   if request.method == 'POST' and af.is_valid():
                      af.q(sqlm)
                return redirect(url_for('viewtable_view', table=table))
                ##########################################
            else:
                return redirect(url_for('viewtable_view', table=table))
        else:
            return redirect(url_for('viewtable_view'))
    else:
        return redirect(url_for('sqlite_view'))





@app.route('/download_file/')
def download_view():
    if os.path.isfile(session['db_path']):
        file_info = open(session['db_path']).read()
        resp = make_response(file_info)
        fname = os.path.basename(session['db_path']).strip()
        resp.headers['Content-Disposition']='attachment;filename="{0}"'.format(fname)
        return resp
    else:
        return redirect(url_for('sqlite_view'))




'''


DEMO PAGES SECTION


'''



@app.route('/demo/',methods=['GET','POST'])
def sqlite_demo_view():
    if not session.get('demo_db_path'):
        dbdesk.gen_rand_name(8)
        sqlm.db_path = session['demo_db_path'] = app.config['DEMO_DB_DIR']+'/demo_'+dbdesk.rand_name+'.db'
        sqlm.init_db()
    else:
        sqlm.db_path = session['demo_db_path']
        sqlm.init_db()

    sitelogo = app.config.get('APP_TITLE')
    terminal = Terminal(request.form)
    trm_data = None

    ########## РОБОТА SQL ТЕРМІНАЛУ #############
    if request.method == 'POST' and terminal.validate():
        trm_data = terminal.q(sqlm)
        if not trm_data:
            flash('Wrong request')
    #########################################
    tables =[item[0] for item in sqlm.q("select name from sqlite_master where type='table' order by name")]
    dbname = sqlm.q("pragma database_list",one=True)
    return render_template('demo/dbman.html',
            dbname=os.path.basename(dbname[2]),
            tables=tables,
            logo = sitelogo,
            sqlt_form=terminal,
            db_path=session.get('demo_db_path') if session.get('demo_db_path') else False)






@app.route('/demo/tables/', methods=['GET','POST'])
@app.route('/demo/tables/<table>/', methods=['GET','POST'])
def viewtable_demo_view(table = None):
    if session.get('demo_db_path'):
        sqlm.db_path = session['demo_db_path']

        sitelogo = app.config.get('APP_TITLE')
        terminal = Terminal(request.form)
        trm_data = None
        ########## РОБОТА SQL ТЕРМІНАЛУ #############
        if request.method == 'POST' and terminal.validate():
            trm_data = terminal.q(sqlm)
            if not trm_data:
                flash('Wrong request')
        #########################################
        if table is None:
            return redirect(url_for('sqlite_demo_view'))
        else:
            tables =[item[0] for item in sqlm.q("select name from sqlite_master where type='table' order by name")]
            dbname = sqlm.q("pragma database_list",one=True)
            columns = sqlm.q("pragma table_info({0})".format(table))
            table_content = sqlm.q("select * from {0}".format(table))
            table_rows = len(table_content)
            if trm_data:
                table_content = trm_data
            return render_template('components/demo/table_content.html',
                    dbname=os.path.basename(dbname[2]),
                    tbname=table,
                    tables=tables,
                    columns=columns,
                    table_content=table_content,
                    table_rows=table_rows,
                    logo = sitelogo,
                    sqlt_form=terminal,
                    db_path=session.get('demo_db_path') if session.get('demo_db_path') else False)
    else:
        return redirect(url_for('sqlite_view'))





@app.route('/demo/tables/<table>/<option>/', methods=['GET','POST'])
def demo_add_entry_view(table = None, option=None):

    if session.get('demo_db_path'):
        sitelogo = app.config.get('APP_TITLE')
        terminal = Terminal(request.form)
        trm_data = None
        options=('add','delete')
        #tables list
        tables = [item[0] for item in sqlm.q("select name from sqlite_master where type='table' order by name")]
        if table in tables:
            ########## SQL TERMINAL WORK #############
            if request.method == 'POST' and terminal.validate():
                trm_data = terminal.q(sqlm)
                if not trm_data:
                    flash('Wrong request')
            #########################################
            table_content = sqlm.q("select * from {0}".format(table))
            columns = sqlm.q("pragma table_info({0})".format(table))
            #table_rows = len(table_content)
            if trm_data:
                table_content = trm_data
            if option in options:
                if option == 'add':
                   # create form backend
                   af = AddEntryForm(formdata=request.form,table=table,columns=columns)
                   if request.method == 'POST' and af.is_valid():
                      af.q(sqlm)
                return redirect(url_for('viewtable_demo_view', table=table))
                ##########################################
            else:
                return redirect(url_for('viewtable_demo_view', table=table))
        else:
            return redirect(url_for('viewtable_demo_view'))
    else:
        return redirect(url_for('sqlite_demo_view'))




@app.route('/exitdb/')
def exitdb_view():
    if session.get('db_path'):
        if os.path.isfile(session.get('db_path')):
            os.unlink(session.get('db_path'))
            session.pop('db_path', None)
            if os.path.isdir(session.get('db_dir')):
                os.rmdir(session.get('db_dir'))
                session.pop('db_dir', None)
    elif session.get('demo_db_path'):
        if os.path.isfile(session.get('demo_db_path')):
            os.unlink(session.get('demo_db_path'))
            session.pop('demo_db_path', None)
    return redirect(url_for('home_view'))





### development and testing page ###
@app.route('/dev/')
def dev_view():
    # testing table
    table = 'languages'
    #getting columns from testing table
    columns = sqlm.q("pragma table_info({0})".format(table))
    # create form backend ex
    FG = FormClassGenerator()
    formbg =FG(columns)
    #test output
    return str([item['notnull'] for item in columns])





@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404


app.secret_key = 'poweirtweoituwporeitkjdghsldkfdkljgh2387421987349128374)(*&)(*&*&*(&(*)'

