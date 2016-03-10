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

    def put(self,command):
        '''
        上传文件
        :param command:
        :return: 返回文件的发送状态（成功/失败）
        '''
        #得到文件的名字、大小、md5值信息
        file_name=command.split('|')[1]
        #如果本地文件存在
        if os.path.isfile(file_name):

            fname=os.path.basename(file_name)
            fsize=os.path.getsize(file_name)
            fmd5=common.encry_file(file_name)
            #客户端发送信息
            send_msg='{cmd}|｛fname｝|{fsize}|{fmd5}'.format(cmd='put',
                                                           fname=fname,
                                                           fsize=fsize,
                                                           fmd5=fmd5)
            self.socket.sendall(bytes(send_msg,'utf-8'))
            recive_server_data=str(self.socket.recv(1024),'utf-8')

            if_can_send=False #是否可以发送标签
            #如果返回文件没有发送过
            if recive_server_data.split('|')[0] == '0':
                if fsize+self.usedspace>self.totalspace:
                    return  'FTP服务器磁盘配额不足，请联系管理员提升磁盘配额'
                else:
                    if_can_send=True
            #否则文件已经发送过
            else:
                if recive_server_data.split('|')[3]==fmd5:
                    return  '目标文件已经存在并且校验与本地一致，无须再发送'
                else:
                    if_can_sen=True
            #如果可以发送
            if if_can_send:
                #try:
                    with open(file_name,'rb') as f:
                        #根据返回获取文件已发送大小
                        sended_size=recive_server_data.split('|')[2]
                        while fsize>sended_size:
                            f.seek(sended_size)
                            send_content=f.read(2048)
                            l=len(send_content)
                            self.socket.send(send_content)
                            sended_size+=l
                            #打印上传进度条
                            common.print_process(fsize,sended_size)
                        #记录日志
                    common.write_log('{0}发送陈功'.format(file_name),'info')
                    return  '文件发送成功'
                    '''
                except Exception as e:
                    #记录日志
                    common.write_log('{0}文件发送失败'.format(file_name),'error')
                    return False'''

            else:
                return '本地文件不存在'








