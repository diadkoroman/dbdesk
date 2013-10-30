# -*- coding: utf-8 -*-
import re
def validate_strdata(data):
    try:
        data = data.strip().encode('UTF-8')
    except:
        data = ''
    finally:
        return data

def validate_intdata(data):
    try:
        data = int(str(data).strip())
    except:
        data = ''
    finally:
        return data


