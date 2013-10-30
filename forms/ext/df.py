# -*- coding: utf-8 -*-
import datetime

class Stack:

    def __init__(self, data):
        self.data = data

    def __call__(self):
        return self.data

class DynamicForm:
    def __init__(self, **kwargs):

        # stack for not validated data
        self._not_validated = {}
        # "parent" table name
        self._table = kwargs['table']
        kwargs.pop('table',None)

        '''
        COLUMNS
        stack of table columns except primary key
        '''
        self.columns = [c for c in kwargs['columns'] if c['pk'] == 0]
        self.colnames = [c['name'] for c in kwargs['columns'] if c['pk'] == 0]
        kwargs.pop('columns',None)

        '''
        DATA NOT VALIDATED
        Stack for not validated data
        '''

        for k, v in kwargs['formdata'].iteritems():
            self._not_validated[k] = v

        '''
        Class entity fields is created according to columns info
        Not validated data is added to special 'nvd' field
        '''

        for col in self.columns:
            attrs = {}
            for k in col.keys():
                attrs[k] = col[k]
            attrs['nvd'] = self._not_validated[col['name']]
            attrs['data'] = None
            setattr(self, col['name'],attrs)

    '''
    do_int
    method to validate int data
    '''
    def do_int(self, data):
        try:
            return int(data)
        except:
            return False

    '''
    do_float
    method to validate float data
    '''
    def do_float(self, data):
        try:
            return float(data)
        except:
            return False

    '''
    do_string
    method to validate string data
    '''
    def do_string(self,data):
        try:
            data = data.encode('UTF-8')
            return str(data)
        except:
            return False

    '''
    do_datetime
    method to validate datetime
    '''
    def do_datetime(self,data):
        try:
            data = datetime.datetime.strftime(data,'%Y-%m-%d %H:%M:%S')
            return str(data)
        except:
            return False

    '''
    is_empty
    method to validate if field is empty
    '''
    def is_empty(self,data):
        try:
            data = data.encode('UTF-8')
        except:
            data = data
        if len(str(data)) == 0:
            return True
        else:
            return False


    '''
    is_valid
    method of all fields data validation
    '''

    def is_valid(self):
        result = True
        for cname in self.colnames:
            attr = getattr(self, cname)
            if not isinstance(attr,(Stack,)):
                if attr['type'] == 'text':
                    data = self.do_string(attr['nvd'])
                elif attr['type'] == 'integer':
                    data = self.do_int(attr['nvd'])
                elif attr['type'] == 'real':
                    data = self.do_float(attr['nvd'])
                elif attr['type'] == 'datetime':
                    #data = datetime.datetime.now().replace(microsecond=0)
                    data = self.do_datetime(attr['nvd'])

                '''
                try to manage notnull option
                ----------------------------
                ----------------------------
                if notnull is set and field in form is empty:
                ---------------------------------------------
                if datetime - set current datetime by python
                else - try to set default value itself
                if data still empty - breaking validation process
                '''
                if attr['notnull']:
                    if self.is_empty(data) or not data:
                        if attr['type'] == 'datetime':
                            data = datetime.datetime.now().replace(microsecond=0)
                        else:
                            if attr['dflt_value']:
                                data = attr['dflt_value']
                        if self.is_empty(data):
                            result = False
                            break

                if not data:
                    result = False
                    break
                else:
                    setattr(self,cname,Stack(data))
            else:
                pass

        return result


class AddEntryForm(DynamicForm):
    def __init__(self, **kwargs):
        DynamicForm.__init__(self, **kwargs)
    '''
    q
    '''
    def q(self,db_engine):
        col=[]
        val=[]
        for cname in self.colnames:
            prop = getattr(self,cname)
            col.append(cname)
            val.append(prop.data)
            prepared = []
            for item in val:
                prepared.append("'{0}'".format(item) if not isinstance(item,(int,)) else str(item))
        query = "insert into {0} ({1}) values ({2})".format(self._table,','.join(col),','.join(prepared))
        db_engine.q(query)
