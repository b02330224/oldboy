#!/usr/bin/env python
#-*-coding:utf-8-*-

import os,sys

FTP_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVER_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(FTP_DIR)
sys.path.append(SERVER_DIR)

USER_INFO_DIR=os.path.join(SERVER_DIR,'db')
USER_INFO_PATH=os.path.join(USER_INFO_DIR,'user.ini')
