#!/usr/bin/env python
#-*-coding:utf-8-*-

import os,sys
import configparser
FTP_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVER_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(FTP_DIR)
sys.path.append(SERVER_DIR)
from conf import setting

#用户文件


class dbhandler(object):
    '''
    用户文件处理
    '''
    def __init__(self):
        self._file=setting.USER_INFO_PATH
config=configparser.ConfigParser()

