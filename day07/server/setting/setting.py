#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
__author__='weiqiang'
blog:http://www.cnblogs.com/weiqiangwang/
'''

import os,sys

BASEDIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASEDIR)

file_db={"dbpath":os.path.join(BASEDIR,'db'),'file_path':{'userinfo':'userinfo.db'}}
print(file_db['dbpath'])