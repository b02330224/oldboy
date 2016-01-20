#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
__author__='weiqiang'
blog:http://www.cnblogs.com/weiqiangwang/
'''
import sys
import json


#检查用户输入格式是否可以被json
def check_input(input_str):
    try:
        json.loads(input_str)
    except:
        return 0

file_name='ha.proxy'
#往文件中追加内容
def file_append(agr):
    with open(file_name,'a+') as x:
        x.write(str(agr))

#读文件内容到一个list(去除每行空格)
def file_read_to_list():
    with open(file_name,'r') as f:
        line_list=[]
        #把文件所有行去除两边空格后读入到一个list中
        for line in f.readlines():
            new_line=line.strip()
            line_list.append(new_line)
    return line_list

#检查输入
def check_inpu(user_input):
    def test_int():
        try:
            int(user_input)
            return 1
        except:
            return 0

    if test_int() and user_input in ['1','2','3','4',]:
        return 1
    else:
        return 0

#功能列表
def function_list():
    print('欢迎使用配置文件修改工具'.center(40,'*'))
    print('（1）查询记录'.center(40))
    print('（2）修改记录'.center(40))
    print('（3）增加记录'.center(40))
    print('（4）删除记录'.center(40))
    while True:
        chioce=input('请选择功能清单编号(输入q退出)：')
        res=check_inpu(chioce)
        if chioce=='q':sys.exit(0)
        elif res==0:
            print('输入有误，请重新输入')
            continue
        elif chioce=='1':find()
        elif chioce=='2':modify()
        elif chioce=='3':add()
        elif chioce=='4':delete()
        else:continue


def find():
    pass

def modify():
    pass

def add():
    while True:
        user_input=input('请输入修改内容，注意使用双引号，（提示：‘{"backend": "test.oldboy.org","record":{"server": "100.1.7.999","weight": 20,"maxconn": 30}}’）')
        if check_input(user_input)==0:
            print('输入格式有误！请重新输入!!!')
            continue
        else:
            dic_input=json.loads(user_input)
            domain=dic_input['backend']#去域名
            server_ip=dic_input['record']['server']#取ip
            weight=dic_input['record']['weight']#获取权重
            maxconn=dic_input['record']['maxconn']#获取最大连接数
            new_line_list=file_read_to_list()#获取文件list
            print(new_line_list)
            backend='backend %s'%domain
            record='server {0} {1} weight {2} maxconn {3}'.format(server_ip,server_ip,weight,maxconn)
            print(record)
            #如果域名不在文件中，则把域名和记录添加到文件
            if backend not in new_line_list:
                file_append(backend)
                file_append('\n'+''*8)
                file_append(record)
                print('添加记录成功！')
                function_list()
            #如果域名在文件中，记录不在文件中，则在文件的下一行添加记录
            elif backend in new_line_list and record not in new_line_list:
                backend_index=new_line_list.index(backend)
                new_line_list.insert(backend_index+1,' '*8+record)
                with open(file_name,'w') as a:
                    a.writelines(new_line_list)
                print('添加记录成功！')
                function_list()
            else:
                print('您要添加的记录已经存在')
                function_list()

def delete():
    pass

if  __name__ == '__main__':
    while True:
        function_list()



