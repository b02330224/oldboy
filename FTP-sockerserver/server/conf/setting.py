#!/usr/bin/env python
#-*-coding:utf-8-*-

import os,sys

FTP_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVER_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(FTP_DIR)
sys.path.append(SERVER_DIR)

#用户数据文件目录
USER_INFO_DIR=os.path.join(SERVER_DIR,'db')
#用户数据文件地址
USER_INFO_PATH=os.path.join(USER_INFO_DIR,'user.ini')
#服务器ip
SERVER_IP='127.0.0.1'
#服务器端口
SERVER_PORT=9999