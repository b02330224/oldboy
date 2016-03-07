#!/usr/bin/env python
#-*-coding:utf-8-*-

import socketserver,os,sys
FTP_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVER_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(FTP_DIR)
sys.path.append(SERVER_DIR)
from common import common
from modules import server



class myserver(socketserver.BaseRequestHandler):

    def handle(self):
        client_socket=self.request
        client_addr = self.client_address
        #发送连接成功标识
        client_socket.sendall(bytes('100','utf8'))
        #客服端连接日志
        common.write_log('client {0} connect the server'.format(client_addr))

        while True:
            client_send_data = str(client_socket.recv(1024),encoding='utf-8')
            #取命令
            client_cmd = client_send_data.split('|')[0]
            #记录操作日志
            common.write_log('client {0} send command {1}'.format(client_addr,client_cmd))
            if client_cmd == 'auth':
                auth_result=server.auth(client_socket,client_send_data)






