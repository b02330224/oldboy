#!/usr/bin/env python
#-*-coding:utf-8-*-

import os
import socketserver,os,sys
FTP_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVER_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(FTP_DIR)
sys.path.append(SERVER_DIR)
from conf import setting
from dbhandler.user_info_api import dbhandler

class User(object):
    '''
    一个FTP用户的类（无论是否登录）
    '''

    db_path=setting.USER_INFO_PATH
    handler=dbhandler(db_path)
    def __init__(self,username):
        self.username = username
        self.exists = False
        self.islocked = 0
        self.passwd = ''
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

        if self.username in User.handler.read_all_sections():
            self.exists = True
            self.__load_user_info()

    def __load_user_info(self):
        '''
        从配置文件加载用户信息，填充对象属性
        :return:
        '''
        self.islocked = User.handler.read_section_option(self.username,'islocked')
        self.passwd = User.handler.read_section_option(self.username,'passwd')
        self.totalspace = User.handler.read_section_option(self.username,'totalspace')
        self.usedspace = User.handler.read_section_option(self.username,'usedspace')


    def auth(self,passwd):
        user_pass=User.handler.read_section_option(self.username,'passwd')
        times=3
        while times>0:
            if passwd == user_pass:
                times=3
                User.handler.write_into_option(self.username,'islocked',0)
                return True
            else:
                times-=1
                return False
        else:
            User.handler.write_into_option(self.username,'islocked',1)

