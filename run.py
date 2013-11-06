# -*- coding: utf-8 -*-
import os, re
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, make_response


app = Flask(__name__)
app.debug = True
app.config.from_object('configs.settings')

# dev version
from dev.dbdeskapp import sqlmd
app.register_blueprint(sqlmd,url_prefix = '/sqlite')

@app.route('/')
def indexview():
    return redirect(url_for('sqlmd.homeview'))

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'),404


app.secret_key = 'poweirtweoituwporeitkjdghsldkfdkljgh2387421987349128374)(*&)(*&*&*(&(*)'
