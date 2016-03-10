#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
__author__='weiqiang'
blog:http://www.cnblogs.com/weiqiangwang/
本模块参考学神王松同学，非完全copy
'''

import socket,os,sys,json
CLINET_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FTP_DIR=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(CLINET_DIR)
sys.path.append(FTP_DIR)
from common import common
from module import client
from conf import setting,template,codes


def main():
    ip_port=(setting.SERVER_IP,setting.SERVER_PORT)

    #初始化一个连接客户端类
    new_client=client.client(ip_port)
    #连接服务器
    connect_flag = True
    while connect_flag:
        if new_client.connect():
            #登录
            new_client.login()
            #登录成功
            while new_client.login_status:
                show_menu=template.LOGINED_MENU.format(new_client.username,
                                                           str(new_client.totalspace/1024/1024),
                                                           str(new_client.usedspace/1024/1024))
                common.show_msg(show_menu,"INFO")
                input_command=common.parser_command('请按提示格式输入命令：')
                if input_command == 'quit':
                    connect_flag = False
                    break
                else:
                    #获取输入的命令
                    get_cmd=input_command.split('|')[0]
                    print(get_cmd)
                    #try:
                    #利用反射调用
                    if hasattr(new_client,get_cmd):
                        get_cmd = getattr(new_client,get_cmd)
                        print('------------111111111')
                        exec_res = get_cmd(new_client,input_command)
                        print('222222222222222222')
                        print(exec_res)
                    else:
                        common.write_log('{0}命令未找到'.format(get_cmd),'error')
                    #except Exception as e:
                     #   common.write_log(e,'error')

if __name__ == '__main__':
    main()






