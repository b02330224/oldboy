#!/usr/bin/env python
#-*-coding:utf-8-*-

import socketserver,os,sys
FTP_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SERVER_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(FTP_DIR)
sys.path.append(SERVER_DIR)
from common import common
from conf.setting import SERVER_IP,SERVER_PORT
from modules import server


class myserver(socketserver.BaseRequestHandler):

    def handle(self):
        try:
            client_socket=self.request
            client_addr = self.client_address
            #发送连接成功标识
            client_socket.sendall(bytes('100','utf8'))
            #客服端连接日志
            common.write_log('client {0} connect the server'.format(client_addr),'info')

            while True:
                #接受用户数据
                client_send_data = str(client_socket.recv(2048),encoding='utf-8')
                print('33333333333333',client_send_data)
                #取命令
                client_cmd = client_send_data.split('|')[0]
                #记录操作日志
                common.write_log('client {0} send command {1}'.format(client_addr,client_cmd),'info')
                if client_cmd == 'auth':
                    client_user=server.auth(client_socket,client_send_data)
                else:
                    if hasattr(server,client_cmd):
                        func=getattr(server,client_cmd)
                        print('main',client_cmd)
                        func(client_socket,client_user,client_send_data)
                        print(client_send_data)
                    else:
                        common.write_log('您输入的命令不存在','ERROE')

        except Exception as e:
            common.write_log(e,'error')



Server=socketserver.ThreadingTCPServer((SERVER_IP,SERVER_PORT),myserver)
Server.serve_forever()



