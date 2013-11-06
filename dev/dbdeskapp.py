# -*- coding: utf-8 -*-
import os,sqlite3
from flask import Blueprint, request, session,render_template, url_for, redirect, flash
import configs.settings as confs
from run import app as devApp

from core.sqlitemanager import SQLiteManager
from core.dbdesk import DBdesk
from forms.sqlterm import SQLTerminal as Terminal
from forms.importdb import ImportDBForm as IDBForm
'''
def connect_db():
    if sqlite3:
        return sqlite3.connect(devApp.config.get('SQLITE_APPDB_PATH'))
        
# get database
def get_db():
    db = connect_db()
    db.row_factory = sqlite3.Row
    return db

def q(query,args=(),one = False):
    q_startswith=('insert','update','delete')
    db = get_db()
    try:
        res = db.cursor().execute(query,args).fetchall()
        if query.startswith(q_startswith):
            db.commit()
            return True
        else:
            return (res[0] if res else None) if one else res
    except:
        return False

# get database name
def get_dbname():
    dbfull = q("pragma database_list",one=True)
    return os.path.basename(dbfull[2])

# get columns
def get_columns(tablename):
    columns = q("pragma table_info({0})".format(tablename))
    return columns
        
# get all table rows
def get_table_content(tablename):
    return q("select * from {0}".format(tablename))

# get tables listing
def get_tables_list():
    items=q("select name from sqlite_master where type='table' order by name")
    return [item[0] for item in items]

# get pk column
def get_pk(columns):
    for c in columns:
        if c['pk'] == 1:
            return c['name']
'''




sqlmd = Blueprint('sqlmd', __name__, template_folder='templates',static_folder='static')

sqlm = SQLiteManager(devApp.config.get('SQLITE_APPDB_PATH'))
dbdesk = DBdesk(config=devApp.config)

@sqlmd.route('/', methods=['GET','POST'])
def homeview():
    # знищуємо вказівники на неіснуючі файли
    if session.get('db_path'):
        if not os.path.isfile(session.get('db_path')):
            session.pop('db_path', None)
            
    sitelogo = devApp.config.get('APP_TITLE')
    terminal = Terminal(request.form)
    idb_form = IDBForm(request.form)
    ########### РОБОТА ІМПОРТУ БД ###########
    if request.method == 'POST' and idb_form.validate():
        file = request.files['db_file']
        if dbdesk.import_database_file(file):
            session['db_dir'] = dbdesk.db_dir
            session['db_path'] = dbdesk.db_path
    ############## якщо є шлях до бд - підключаємо термінал ##################
    if session.get('db_path') and os.path.isfile(session.get('db_path')):
        sqlm.dbpath = session['db_path']
        try:
            ########## РОБОТА SQL ТЕРМІНАЛУ #############
            if request.method == 'POST' and terminal.validate():
                trm_data = terminal.q(sqlm)
                if not trm_data:
                    flash('Wrong request')
            #########################################
            tables = sqlm.get_tables_list()
            dbname = sqlm.get_dbname()
            
            return render_template('dbman.html',
            dbname=dbname,
            tables=tables,
            logo = sitelogo,
            sqlt_form=terminal,
            db_path=session.get('db_path') if session.get('db_path') else False)
        except:
            return 'path managed'
    else:
        return render_template('import_db.html',logo = sitelogo,idb_form=idb_form)


@sqlmd.route('/tables/', methods=['GET','POST'])
@sqlmd.route('/tables/<table>/', methods=['GET','POST'])
def viewtable_view(table = None, option = None):
    
    sitelogo = devApp.config.get('APP_TITLE')
    terminal = Terminal(request.form)
    trm_data = None
    ########## SQL TERMINAL WORK #############
    if request.method == 'POST' and terminal.validate():
        trm_data = terminal.q(sqlm)
        if not trm_data:
            flash('Wrong request')
    #########################################
    if session.get('db_path'):
        sqlm.dbpath = session['db_path']
        tables = sqlm.get_tables_list()
        dbname = sqlm.get_dbname()
        if table:
            columns = sqlm.get_columns(table)
            table_content = sqlm.get_table_content(table)
            table_rows = len(table_content)
            if trm_data and not isinstance(trm_data,(bool,)):
                table_content = trm_data

            return render_template('components/table_content.html',
                    dbname=dbname,
                    tbname=table,
                    tables=tables,
                    columns=columns,
                    table_content=table_content,
                    table_rows=table_rows,
                    logo = sitelogo,
                    sqlt_form=terminal,
                    db_path=session.get('db_path') if session.get('db_path') else False)
        else:
            return redirect(url_for('.homeview'))

    else:
        return redirect(url_for('.homeview'))


@sqlmd.route('/download_file/')
def download_view():
    if os.path.isfile(session['db_path']):
        file_info = open(session['db_path']).read()
        resp = make_response(file_info)
        fname = os.path.basename(session['db_path']).strip()
        resp.headers['Content-Disposition']='attachment;filename="{0}"'.format(fname)
        return resp
    else:
        return redirect(url_for('.homeview'))

@sqlmd.route('/exitdb/')
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
    return redirect(url_for('.homeview'))


'''


DEMO PAGES SECTION


'''


@sqlmd.route('/demo/',methods=['GET','POST'])
def demo_index_view():
    if not session.get('demo_db_path'):
        dbdesk.gen_rand_name(8)
        sqlm.dbpath = session['demo_db_path'] = devApp.config['DEMO_DB_DIR']+'/demo_'+dbdesk.rand_name+'.db'
        sqlm.init_db()
    else:
        sqlm.dbpath = session['demo_db_path']
        sqlm.init_db()

    sitelogo = devApp.config.get('APP_TITLE')
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






@sqlmd.route('/demo/tables/', methods=['GET','POST'])
@sqlmd.route('/demo/tables/<table>/', methods=['GET','POST'])
def demo_viewtable_view(table = None):
    if session.get('demo_db_path'):
        sqlm.dbpath = session['demo_db_path']

        sitelogo = devApp.config.get('APP_TITLE')
        terminal = Terminal(request.form)
        trm_data = None
        ########## РОБОТА SQL ТЕРМІНАЛУ #############
        if request.method == 'POST' and terminal.validate():
            trm_data = terminal.q(sqlm)
            if not trm_data:
                flash('Wrong request')
        #########################################
        if table is None:
            return redirect(url_for('.demo_index_view'))
        else:
            # get tables listing
            tables=sqlm.get_tables_list()
            
            #get db name
            dbname=sqlm.get_dbname()
            
            #get columns from current table
            columns = sqlm.get_columns(table)
            
            #get table content from current table
            table_content = sqlm.get_table_content(table)
            
            table_rows = len(table_content)
            if isinstance(trm_data,(dict,list,tuple)):
                table_content = trm_data
            return render_template('components/demo/table_content.html',
                    dbname=dbname,
                    tbname=table,
                    tables=tables,
                    columns=columns,
                    table_content=table_content,
                    table_rows=table_rows,
                    logo = sitelogo,
                    sqlt_form=terminal,
                    db_path=session.get('demo_db_path') if session.get('demo_db_path') else False)
    else:
        return redirect(url_for('.homeview'))





@sqlmd.route('/demo/tables/<table>/<option>/', methods=['GET','POST'])
def demo_options_view(table = None, option=None):

    if session.get('demo_db_path'):
        sitelogo = devApp.config.get('APP_TITLE')
        terminal = Terminal(request.form)
        trm_data = None
        options=('add','delete')
        #tables list
        tables=sqlm.get_tables_list()
        if table in tables:
            ########## SQL TERMINAL WORK #############
            if request.method == 'POST' and terminal.validate():
                trm_data = terminal.q(sqlm)
                if not trm_data:
                    flash('Wrong request')
            #########################################
            table_content = sqlm.get_table_content(table)
            columns = sqlm.get_columns(table)
            #table_rows = len(table_content)
            if isinstance(trm_data,(dict,list,tuple)):
                table_content = trm_data
            if option in options:
                if option == 'add': # adding entry
                   # create form backend
                   af = AddEntryForm(formdata=request.form,table=table,columns=columns)
                   if request.method == 'POST' and af.is_valid():
                      af.q(sqlm)
                      
                elif option == 'delete': # deleting entry
                    sqlm.q('delete from `%s` where id = %d' % (table,int(request.args.get('id'))))
                    
                elif option == 'update': #updating entry
                    uf = UpdateEntryForm(formdata=request.form,table=table,columns=columns)
                    if request.method == 'POST' and uf.is_valid():
                        uf.q(sqlm)
                return redirect(url_for('.demo_viewtable_view', table=table))
                ##########################################
            else:
                return redirect(url_for('.demo_viewtable_view', table=table))
        else:
            return redirect(url_for('.demo_viewtable_view'))
    else:
        return redirect(url_for('.demo_index_view'))
            
