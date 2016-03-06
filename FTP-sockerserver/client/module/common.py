#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
__author__='weiqiang'
blog:http://www.cnblogs.com/weiqiangwang/
系统公共模块
"""
import datetime,io,sys,hashlib
from conf import setting

def write_log(content,tytes):
    '''
    日志记录
    :param content: 具体日志信息
    :param tytes: 消息类型，info，error
    :return: 无返回
    '''
    _content='\n{0} - {1} - {2}'.format(datetime.datetime.now().strftime('%Y-%m-%d %X'),tytes,content)
    with open(setting.CLIENT_LOG,'a+') as f:
        f.write(_content)

def encry_sha1(file):
    '''
    文件MD5校验
    :param str: 文件名
    :return: 返回加密文件的MD5值
    '''
    f_md5=hashlib.md5()
    file=io.FileIO(file,'r') #二进制读取文件
    byte=file.read(2048)
    while byte != b'':
        f_md5.update(byte)
        byte=file.read(2048)
    file.close()
    encry_res=f_md5.hexdigest()
    return encry_res


def encry_str(str):
    '''
    此函数主要为密码加密使用
    :param str:
    :return:
    '''
    sha=hashlib.sha224()
    sha.update(str.encode())
    sha_res=sha.hexdigest()
    return sha_res


def show_msg(msg,msgtype):
    '''
    根据不同的消息类型选择不通的颜色，相当于封装了print函数
    :param content: 要显示的消息
    :param types: 消息类型
    :return:
    '''
    if msgtype == "NOTICE":
        show_msg = "\n\033[1;33m{0}\033[0m\n".format(msg)
    elif msgtype == "ERROR":
        show_msg = "\n\033[1;31m{0}\033[0m\n".format(msg)
    elif msgtype == "INFO":
        show_msg = "\n\033[1;32m{0}\033[0m\n".format(msg)
    else:
        show_msg = "\n{0}\n".format(msg)
    print(show_msg)


def input_check(msg,limit_value):
    '''
    检查用户的输入，为空继续输入，不为空则返回输入信息，相当于封装了input函数
    :param msg: input 函数日的提示信息
    :param limit_value: 限制输入信息的类型，必须为limit_value定义的值
    :return: 返回输入信息
    '''
    while True:
        input_value=input(msg).strip()
        if not input_value:
            show_msg('输入不能为空','ERROR')
            continue
        elif len(input_value)>0:
            if input_value not in limit_value:
                show_msg('输入值不正确,请重新输入','ERROR')
                continue
            else:
                return input_value


def parser_command(msg):
    '''
    解析用户输入的命令
    :param msg: 提示信息
    :return: 返回处理后的格式化命令
    '''
    flag=True
    while flag:
        limit_value=['show','cd','get','put','quit']
        input_command=input_check(msg).strip()

        if input_command== 'show':
            return_command='show|'
        elif input_command == 'quit':
            return_command = 'quit'
        else:
            if input_command.count('|')!=1:
                show_msg('你输入的命令不合法，请重新输入','NOTICE')
                continue
            else:
                cmd=input_command.split('1')[0].strip().lower()
                agrs=input_command.split()[1].strip()
                if cmd not in limit_value:
                    show_msg('您输入的命令不存在，请重新输入','ERROR')
                    continue
                else:
                    return_command='{0}|{1}'.format(cmd,agrs)
                    flag=False
    return return_command

def print_proccess(totalsize,curr_size):
    '''
    打印进度条信息
    :param totalsize: 文件总大小
    :param curr_size: 文件当前大小
    :return:
    '''
    c=int((curr_size/totalsize)*66)
    p=int(curr_size/totalsize*100)
    j='--'*66
    sys.stdout.write('当前传输进度：｛0｝% || ｛1｝'.format(str(p),j))



