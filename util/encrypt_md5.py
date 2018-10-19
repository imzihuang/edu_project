#!/usr/bin/python
# -*- coding: UTF-8 -*-


import hashlib

def encry_md5(v):
    m = hashlib.md5()
    m.update(v)
    return m.hexdigest()