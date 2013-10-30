# -*- coding: utf-8 -*-
import datetime
from wtforms import Form, BooleanField, TextField, IntegerField, DateField, DateTimeField, DecimalField, FloatField, validators

### Factory for dynamic form backend generation ###
def FormClassGenerator():
    class AddEntryForm(Form):
        def __init__(cls,**kwargs):
            super(AddEntryForm,cls).__init__(**kwargs)
            #
            columns = [c for c in kwargs['columns'] if c['pk'] == 0]
            colnames = [c['name'] for c in columns]
            #self._fields = {}
            _table = kwargs['table']
            #
            for column in columns:
                vldts = []
                if column['notnull'] == 1:
                    vldts.append(validators.required())
                setattr(cls,column['name'],None)

                if column['type'] == 'integer':
<<<<<<< HEAD
                    getattr(cls,column['name'], IntegerField('',vldts))

                elif column['type'] == 'real':
                    getattr(cls,column['name'], DecimalField('',vldts))

                elif column['type'] == 'text':
                    getattr(cls,column['name'], TextField('',vldts))

                elif column['type'] == 'datetime':
                    getattr(cls,column['name'], DateTimeField('',vldts))

                elif column['type'] == 'date':
                    getattr(cls,column['name'], DateField('',vldts))

        def q(self,sqlm):
            if self.validate():
                return str(self.title.data)





    return AddEntryForm
=======
                    getattr(self, column['name'], IntegerField(column['name'],self.set_validators(column)))
                elif column['type'] == 'real':
                    getattr(self, column['name'], FloatField(column['name'],self.set_validators(column)))
                elif column['type'] == 'text':
                    getattr(self, column['name'], TextField(column['name'],self.set_validators(column)))

        def set_validators(column):
            vldts=[]
            for key,val in column.iteritems():
                if key == 'notnull':
                    if val == 0:
                        self.vldts + validators.required()
            return vldts
>>>>>>> dfec2f5e83be2a14569953cd04ccf8748c9f0efb


    return DForm
