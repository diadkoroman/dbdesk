# -*- coding: utf-8 -*-
from dbdesk.runner import make_query

def q(trm):
    query = trm.terminal_data.data.lower().replace(';','')
    table_content = make_query(trm.terminal_data.data)
    if table_content:
        return table_content
    else:
        return False
