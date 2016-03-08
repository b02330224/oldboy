#!/usr/bin/env python
#-*-coding:utf-8-*-

import os,sys
import configparser
FTP_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVER_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(FTP_DIR)
sys.path.append(SERVER_DIR)
from conf import setting
from common import common

#用户文件


class dbhandler(object):
    '''
    用户文件文件增删改查处理
    '''
    def __init__(self,file_path):
        self._file=file_path
        self.config=configparser.ConfigParser()
        self.read=self.config.read(self._file)

    #读取文件的sections
    def read_all_sections(self):
        '''
        返回所有section
        :return:
        '''
        all_sections=self.config.sections()
        return all_sections

    #读取指定section的所有options
    def read_special_section(self,username):
        '''
        返回指定section的所有option列表
        :param username:
        :return:
        '''
        options=self.config.items(username)
        return options

    #读取指定sections里指定option的值
    def read_section_option(self,section,option):
        option_value=self.config.get(section,option)
        return option_value

    #更新指定section,option配置文件
    def write_into_option(self,section,option,value):
        try:
            self.config.set(section,option,value)
            with open(self._file,'w+') as f:
                self.config.write(f)
            common.write_log('更新{0}的{1}为{2}'.format(section,option,value),'INFO')
        except Exception as e:
            common.write_log(e,'error')




