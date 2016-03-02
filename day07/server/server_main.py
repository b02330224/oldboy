#!/usr/bin/env python
#-*-coding:utf-8-*-

import socket
from oldboy.day07.server.login_server.login_auth import login_auth



#userinfo_file=

ip_port=('127.0.0.1',9999)
server_sk=socket.socket()
server_sk.bind(ip_port)
server_sk.listen(5)
while True:
    print('server is waiting....')
    conn,addr=server_sk.accept()
    client_data=str(conn.recv(1024),encoding='utf-8')
    conn.send(bytes('established','utf8'))
    res=login_auth(conn)
    server_sk.close()