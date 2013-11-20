# -*- coding: utf-8 -*-
from wtforms import Form, BooleanField, FileField, validators
import re
class ImportDBForm(Form):
    #db_file = FileField('Input your file',[validators.required()])
    agreement = BooleanField('I understand all risks',[validators.required(),validators.AnyOf((True,'yes'))])









