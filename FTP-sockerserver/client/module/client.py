#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
__author__='weiqiang'
blog:http://www.cnblogs.com/weiqiangwang/
'''
import socket,os,sys,json
CLIENT_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FTP_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(CLIENT_DIR)
sys.path.append(FTP_DIR)
from common import common
from conf import setting
from conf.codes import MSG_CODES

class client(object):

    def __init__(self,ip_port):
        self.__down_path = setting.DOWNLOAD_DIR
        self.username = ''
        self.login_status = False
        self.totalspace = 0
        self.usedspace = 0
        self._server = (ip_port)
        self.socket = socket.socket()

    def connect(self):
        '''
        SOCKET连接
        :return:返回连接状态
        '''
        self.socket.connect(self._server)
        recive_server_data=str(self.socket.recv(1024),'utf-8')
        if recive_server_data == MSG_CODES['CONN_SUCC']['num']:

            return True
        else:
            common.show_msg(MSG_CODES['CONN_FAIL']['DESC'],'ERROR')
            return False
    def login(self):
        '''
        客户端登录，根据server返回值判断提示用户
        200：登录成功
        201：登录失败
        202：用户不存在
        203：用户被锁定
        :param username:
        :param passwd:
        :return: 返回用户的登录状态
        '''
        while not self.login_status:
            username=common.input_check('请输入你的用户名：')
            input_passwd=common.input_check('请输入您的密码：')
            #密码加密
            passwd=common.encry_str(input_passwd)

            sendmsg='{cmd}|{username}|{passwd}'.format(cmd='auth',username=username,passwd=passwd)
            self.socket.sendall(bytes(sendmsg,'utf-8'))
            auth_status = str(self.socket.recv(1024),'utf-8')
            print(auth_status)

            #登录成功
            if auth_status == MSG_CODES['AUTH_SUCC']['num']:
                self.login_status = True
                self.username = username
                space_info = str(self.socket.recv(100),encoding='utf8')
                self.totalspace = int(space_info.split("|")[0])
                self.usedspace = int(space_info.split("|")[1])
                common.show_msg(MSG_CODES['AUTH_SUCC']['DESC'],'INFO')
                return self.login_status
            #密码验证失败
            if auth_status == MSG_CODES['AUTH_FAIL']['num']:
                common.show_msg(MSG_CODES['AUTH_FAIL']['DESC'],'ERROR')
            #用户名不存在
            if auth_status == MSG_CODES['USER_NOT_EXIST']['num']:
                common.show_msg(MSG_CODES['USER_NOT_EXIST']['DESC'],'ERROR')
            #用户被锁定
            if auth_status == MSG_CODES['USER_LOCKED']['num']:
                common.show_msg(MSG_CODES['USER_LOCKED']['DESC'],'ERROR')


