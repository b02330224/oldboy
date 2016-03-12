#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
__author__='weiqiang'
blog:http://www.cnblogs.com/weiqiangwang/
'''

WELCOM_MEMU='''
--------------------------------------------------------
             FTP  CLIENT
--------------------------------------------------------
'''

LOGINED_MENU='''
-------------------------------------------------------------------
                       FTP CLIENT
user:{0}          TolalSpace:{1}MB             UsedSpace:{2}MB
-------------------------------------------------------------------
Commands:
    put: put|[filename]     #upload a file to server
    get: get|[filename]     #download a file to localhost
    show: show              #show all files in the current dir
    cd:   cd|[dir]          #go to [folder],return back dir use 'cd|..'
    quit: quit
'''