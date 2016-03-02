#!/usr/bin/env python
#-*-coding:utf-8-*-

import json,os



class user_db_handler(object):

    __file_name='userinfo.db'
    def __init__(self):
        pass

    def load_all_userinfo(self):
        with open(self.__file_name,'r') as f:
            return json.load(f)

    def load_userinfo(self,user_name):
        '''
        加载某用户的信息
        :param 用户名
        :return 用户信息
        '''
        with open(self.__file_name,'r') as f:
            userinfo=json.load(f)
            return userinfo[user_name]

    def write_into_file(self,content,user_name):
        '''
        更新用户信息
        :param content:
        :return:
        '''
        info= self.load_all_userinfo()
        info[user_name]=content
        with open(self.__file_name,'w+') as f:
            json.dump(info,f)

    def append_into_file(self):
        pass

