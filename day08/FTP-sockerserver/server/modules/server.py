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
    :return: 返回连接用户对象
    '''
    username=client_send_data.split('|')[1]
    passwd=client_send_data.split('|')[2]

    client_user=user.User(username)
    #用户存在
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
    client_socket.sendall(bytes(auth_status,encoding='utf8'))
    if auth_status == '200':
        client_socket.sendall(bytes(user_sapce,encoding='utf8'))
    return client_user

def put(client_socket,client_user,client_data):
    '''
    处理上传信息
    :param client_socket:
    :param clinet_send_data:
    :return: 返回上传状态（成功/失败）
    '''
    #接受客户端信息
    #解析文件信息
    print(client_data)
    fname=client_data.split('|')[1]
    fsize=int(client_data.split('|')[2])
    fmd5=client_data.split('|')[3]

    #设置是否接受标记
    if_recv=False

    #用户家目录文件路径
    file_path=os.path.join(client_user.homedir,fname)

    #文件存在了
    if os.path.exists(file_path):
        local_fsize=os.path.getsize(file_path)
        local_fmd5=common.encry_md5(file_path)
        return_msg='{exist}|{fname}|{fsize}|{fmd5}'.format(exist='1',
                                                           fname=fname,
                                                           fsize=local_fsize,
                                                           fmd5=local_fmd5)
        #如果MD5校验相等，则不接受文件
        if fmd5==local_fmd5:
            client_socket.sendall(bytes(return_msg,encoding='utf8'))
        else:
            if_recv=True
            client_socket.sendall(bytes(return_msg,encoding='utf8'))
    #文件不存在
    else:
        local_fsize=0
        if_recv=True
        return_msg='{exist}|{fname}|{fsize}|{fmd5}'.format(exist='0',
                                                           fname=fname,
                                                           fsize='0',
                                                           fmd5='0')
        print('return_msa',return_msg)
        client_socket.sendall(bytes(return_msg,encoding='utf8'))
    print(if_recv)
    if if_recv:
        try:
            with open(file_path,'ab') as f:
                print('9888888888888888888888')
                f.seek(local_fsize)
                print(local_fsize)
                print('fsize',fsize)
                print(type(fsize))
                while fsize>local_fsize:
                    print('9999999999999999999')
                    r=client_socket.recv(2048)
                    print('++++++++++++++++++++++',str(r))
                    f.write(r)
                    local_fsize+=len(r)

                    if r==b'':
                        common.write_log('{0}文件遇到意外中断，文件上传未完成'.format(fname),'error')
                        break
                else:
                    common.write_log('{0}文件接收完成'.format(fname),'info')
        except Exception as e:
             common.writelog(str(e), "error")


