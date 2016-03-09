#!/usr/bin/env python
#-*-coding:utf-8-*-

import socketserver,os,sys
FTP_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVER_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL_DIR=os.path.join(SERVER_DIR,'modules')
sys.path.append(FTP_DIR)
sys.path.append(SERVER_DIR)
sys.path.append(LOCAL_DIR)
from common import common
import user

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
    print(client_user.times)
    print(type(client_user.times))
    if client_user.exists:
        #用户被锁
        if not client_user.times:
            auth_status='203'
        #密码正确
        elif client_user.auth(passwd):
            user_sapce='{0}|{1}'.format(client_user.totalspace,client_user.usedspace)
            auth_status='200'
        #密码错误
        else:
            auth_status = '201'
    #用户不存在
    else:
        auth_status='202'
    print(auth_status)
    client_socket.sendall(bytes(auth_status,encoding='utf8'))
    if auth_status == '200':
        client_socket.sendall(bytes(user_sapce,encoding='utf8'))
    return client_user
