#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
__author__='weiqiang'
blog:http://www.cnblogs.com/weiqiangwang/
'''
import os,sys

BASEDIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)

#SERVER INFO
SERVER_IP='127.0.0.1'

SERVER_PORT=9999

CLIENT_LOG=os.path.join(BASEDIR,'logs/client.log')

DOWNLOAD_DIR=os.path.join(BASEDIR,'file_dir')