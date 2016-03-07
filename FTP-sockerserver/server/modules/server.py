#!/usr/bin/env python
#-*-coding:utf-8-*-

import socketserver,os,sys
FTP_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVER_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(FTP_DIR)
sys.path.append(SERVER_DIR)
from common import common
from modules import server,user

def auth(client_socket,client_send_data):
    '''
    服务端认证
    :param client_socket:
    :param client_send_data:
    :return:
    '''
    username=client_send_data.split('|')[1]
    passwd=client_send_data.split('|')[2]

    client_user=user.User(username)
    #用户存在
    if client_user.exist:
        #用户是否被锁
        if client_user.is_locked:
            auth_status='203'
        elif client_user.auth(passwd):
            user_sapce='{0}|{1}'.format(client_user.totalspace,client_user.usedspace)
            auth_status='200'
        else:
            auth_status='201'
    #用户不存在
    else:
        auth_status='202'
