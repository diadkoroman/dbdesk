# -*- coding: utf-8 -*-
import os,sqlite3
from flask import Blueprint, request, session,render_template, url_for, redirect, flash, make_response
import configs.settings as confs
from run import app

from core.sqlitemanager import SQLiteManager, SQLiteManager2
from core.dbdesk import DBdesk
from forms.sqlterm import SQLTerminal as Terminal
from forms.importdb import ImportDBForm as IDBForm





sqlmd = Blueprint('sqlmd', __name__, template_folder='templates',static_folder='static')

sqlm = SQLiteManager2(app.config.get('SQLITE_APPDB_PATH'))
dbdesk = DBdesk(config=app.config)

@sqlmd.route('/', methods=['GET','POST'])
def homeview():
    # знищуємо вказівники на неіснуючі файли
    if session.get('db_path'):
        if not os.path.isfile(session.get('db_path')):
            session.pop('db_path', None)

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
    if session.get('db_path') and os.path.isfile(session.get('db_path')):
        sqlm.dbpath = session['db_path']
        try:
            ########## РОБОТА SQL ТЕРМІНАЛУ #############
            if request.method == 'POST' and terminal.validate():
                trm_data = terminal.q(sqlm)
                if not trm_data:
                    flash('Wrong request')
            #########################################
            tables = sqlm.tables
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

    sitelogo = app.config.get('APP_TITLE')
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
        tables = sqlm.tables
        dbname = sqlm.get_dbname()
        if table:
            columns = sqlm.get_columns_list(table)
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
        demodbpath = session['demo_db_path'] = app.config['DEMO_DB_DIR']+'/demo_'+dbdesk.rand_name+'.db'
        sqlm = SQLiteManager2(demodbpath)
        sqlm.create_demodb()
    else:
        sqlm = SQLiteManager2(session['demo_db_path'])

    sitelogo = app.config.get('APP_TITLE')
    terminal = Terminal(request.form)
    trm_data = None

    ########## РОБОТА SQL ТЕРМІНАЛУ #############
    if request.method == 'POST' and terminal.validate():
        trm_data = terminal.q(sqlm)
        if not trm_data:
            flash('Wrong request')
    #########################################
    tables = sqlm.tables
    dbname = sqlm.get_dbname()
    return render_template('demo/dbman.html',
            dbname=dbname,
            tables=tables,
            logo = sitelogo,
            sqlt_form=terminal,
            db_path=session.get('demo_db_path') if session.get('demo_db_path') else False)






@sqlmd.route('/demo/tables/', methods=['GET','POST'])
@sqlmd.route('/demo/tables/<table>/', methods=['GET','POST'])
def demo_viewtable_view(table = None):
    if session.get('demo_db_path'):
        sqlm = SQLiteManager2(session['demo_db_path'])
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
            return redirect(url_for('.demo_index_view'))
        else:
            # get tables listing
            tables=sqlm.tables

            #get db name
            dbname=sqlm.get_dbname()

            #get columns from current table
            columns = sqlm.get_columns_list(table)

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
        sitelogo = app.config.get('APP_TITLE')
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

