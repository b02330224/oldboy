#!/usr/bin/env python
#-*-coding:utf-8-*-

import hashlib

def encrypt(str):
    hash=hashlib.sha1()
    hash.update(str)
    hash_res=hash.hexdigest()
    return hash_res