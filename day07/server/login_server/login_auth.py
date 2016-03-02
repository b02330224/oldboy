#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
__author__='weiqiang'
blog:http://www.cnblogs.com/weiqiangwang/
'''
from oldboy.day07.common import common
from oldboy.day07.server.dbhandler.db_handler import *
import hashlib

f=user_db_handler()

def get_user_pass_sha1(user_name):
    '''
    获取用户名和密码的MD5的加密值
    :param user_name:
    :return:
    '''
    a=user_db_handler()
    b=a.load_userinfo(user_name)
    hash=hashlib.md5()
    hash.update(user_name)
    hash.update(b['passwd'])
    c=hash.hexdigest()
    return c

def login_auth(conn):
    while True:
        client_data=str(conn.recv(5096),encoding='utf-8')
        userinfo=json.loads(client_data)
        times=3
        for k,v in userinfo.items():
            #查看用户是否存在
            if k not in f.load_all_userinfo():
                conn.send(bytes('0','utf8'))
            #判断是否锁定
            elif f.load_userinfo(k)['islocked']==1:
                conn.send(bytes('3','utf8'))
            #如果用户名密码匹配

            else:
                while times>0:
                    #如果匹配发送1
                    if common.encrypt(f.load_userinfo(k)['password'])==userinfo[k]['password']:
                        conn.send(bytes('1','utf8'))
                        return True
                    else:
                        times-=1
                        conn.send(bytes('2','utf8'))
                else:
                    userinfo_k=f.load_userinfo(k)
                    userinfo_k['islocked']=1
                    f.write_into_file(userinfo_k,k)