# -*- coding: utf-8 -*-
import random

RAND_ITEMS='qQwWeErRtTyYuUiIoOpPaAsSdDfFgGhHjJkKlLzZxXcCvVbBnNmM1234567890qQwWeErRtTyYuUiIoOpPaAsSdDfFgGhHjJkKlLzZxXcCvVbBnNmM1234567890'
DEFAULT_SECRETKEY_LENGTH=24

def secretkey(key_length=None):
    if key_length and isinstance(key_length,(int,)):
        sk=random.sample(RAND_ITEMS,key_length)
    else:
        sk=random.sample(RAND_ITEMS,DEFAULT_SECRETKEY_LENGTH)
    return sk

def random_name(key_length = None):
    if key_length and isinstance(key_length,(int,)):
        sk=random.sample(RAND_ITEMS,key_length)
    else:
        sk=random.sample(RAND_ITEMS,DEFAULT_SECRETKEY_LENGTH)
    return ''.join(sk)    
