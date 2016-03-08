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
        self.islocked = False
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
        if self.username in handler.read_all_sections():
            self.exists = True
            self.__load_user_info()

    def __load_user_info(self):
        '''
        从配置文件加载用户信息，填充对象属性
        :return:
        '''
        user_info = handler.read_special_section(self.username)
        self.islocked = user_info['islocked']
        self.passwd = user_info['passwd']
        self.totalspace = user_info['totalspace']
        self.usedspace = user_info['usedspace']



    @property
    def islocked(self):
        '''
        判断用户是否被锁定
        :return: 返回用户的锁定作态
        '''
        is_locked=handler.read_section_option(self.username,'islocked')
        if is_locked == 1:
            return True
        else:
            return False

    def auth(self,passwd):
        user_pass=handler.read_section_option(self.username,'passwd')
        times=3
        while times>0:
            if passwd == user_pass:
                times=3
                handler.write_into_option(self.username,'islocked',0)
                return True
            else:
                times-=1
                return False
        else:
            handler.write_into_option(self.username,'islocked',1)

