#!/usr/bin/env python
#-*-coding:utf-8-*-

import socket
import loginServer
import SocketServer,json
import loginServer

class MyServer(SocketServer.BaseRequestHandler):
    def handle(self):
        # print self.request,self.client_address,self.server
        conn = self.request
        conn.sendall('您已建立ftp连接！')
        Flag = True
        authorized = False
        authorizedDir = ''
        while Flag:
            jmsgClient = conn.recv(1024)
            msgClient = json.loads(jmsgClient)
            if msgClient['request'] == 'login':
                result,authorizedDir = loginServer.login(msgClient['user'],msgClient['password'])
                if result == '1':
                    authorized = True
                    print authorizedDir
                conn.sendall(result)
            if msgClient['request'] == 'exit':
                Flag = False
            elif authorized and msgClient['request'] == 'upload':
                conn.sendall('received')
                base_path = Authorization.chooseDir(conn,authorizedDir)
                for file in range(msgClient['fileCount']):
                    jmsgClient = conn.recv(1024)
                    msgClient = json.loads(jmsgClient)
                    dealwithFileServer.receiveUpload(conn,msgClient['strmd5'],msgClient['fileSize'],msgClient['fileName'],base_path)
                print 'upload finished'
            elif authorized and msgClient['request'] == 'download':
                print msgClient['request']
                dealwithFileServer.receiveDownlode(conn,authorizedDir)
        conn.close()
        print 'conn is closed'

if __name__ == '__main__':
    server = SocketServer.ThreadingTCPServer(('127.0.0.1',8009),MyServer)
    server.serve_forever()
