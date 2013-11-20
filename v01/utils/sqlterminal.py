# -*- coding: utf-8 -*-

def q(trm,q):
    query = trm.terminal_data.data.lower().replace(';','')
    table_content = q(trm.terminal_data.data)
    if table_content:
        return table_content
    else:
        return False
