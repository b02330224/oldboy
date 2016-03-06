#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
__author__='weiqiang'
blog:http://www.cnblogs.com/weiqiangwang/
'''

import json,socket
from day07 import common



def login_cli(cli_sk):
    while True:
        login_result=False
        login_name=input('请输入您的用户名：')
        login_passwd=input('请输入您的密码：')
        if login_passwd:
            passwd_sha1=common.encrypt(login_passwd)
            login_info={login_name:{'password':passwd_sha1}}
            str_login_info=json.dumps(login_info)
            cli_sk.send(str_login_info)
            recv_res=cli_sk.recv(1024)
            if recv_res=='1':
                login_result=True
                print('登录成功')
                return login_result
            elif recv_res=='2':
                print('密码有误，请重新输入，错误三次将被锁定')
                continue
            elif recv_res=='3':
                print('您输入的用户名已被锁定')
            elif recv_res=='0':
                print('您输入的用户名不存在')


ip_port=('localhost',9999)
cli_sk=socket.socket()
cli_sk.connect(ip_port)
cli_sk.send('Request to establish a connection')
server_data=cli_sk.recv(1024)
print(server_data)
login_cli(cli_sk)
