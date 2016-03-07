#!/usr/bin/env python
#-*-coding:utf-8-*-

import os
import socketserver,os,sys
FTP_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVER_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(FTP_DIR)
sys.path.append(SERVER_DIR)
from conf import setting

class User(object):
    '''
    一个FTP用户的类（无论是否登录）
    '''
    def __init__(self,username):
        self.username = username
        self.passwd = ''
        self.exist = False
        self.islocked = 0
        self.totalspace = 0
        self.usedspace = 0
        #用户家目录
        self.homedir = os.path.join(setting.SERVER_DIR,self.username)
        self.__check_user()

    def __check_user(self):
        '''
        检查用户是否存在，
        :return:
        '''
