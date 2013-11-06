# -*- coding: utf-8 -*-
from wtforms import Form, TextAreaField, validators
class SQLTerminal(Form):
    terminal_data = TextAreaField('Put your request here',[validators.required()])
    def q(self, sqlm):
        if self.validate():
            query = self.terminal_data.data.lower().replace(';','')
            try:
                trm_data = sqlm.q(query)
                if not isinstance(trm_data,(list,dict,tuple)) or len(trm_data) == 0:
                    trm_data = True
            except:
                trm_data = False
            finally:
                return trm_data

