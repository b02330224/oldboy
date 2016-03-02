#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
__author__='weiqiang'
blog:http://www.cnblogs.com/weiqiangwang/
'''


import os,sys,json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from setting import setting

_user_list = {
    "mugeda": {"password": "12345","islocked": 0,"role": "user"},
    'mugeda1':{"password": "12345", "islocked": 0, "role": "admin"}
}


#初始化用户信息
def init_userinfo():
    userdb_file=os.path.join(setting.file_db['dbpath'],'userinfo.db')
    with open(userdb_file,'w') as f:
        json.dump(_user_list,f)

init_userinfo()