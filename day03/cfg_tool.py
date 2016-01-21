#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
__author__='weiqiang'
blog:http://www.cnblogs.com/weiqiangwang/
'''
import sys
import json

file_name='ha.proxy'

#检查用户输入格式是否可以被json
def check_input(input_str):
    try:
        json.loads(input_str)
    except:
        return 0


#往文件中追加内容
def file_append(agr):
    with open(file_name,'a+') as x:
        x.write(str(agr))

#读文件内容到一个list
def file_read_to_list():
    with open(file_name,'r') as f:
        line_list=[]
        #把文件所有行去除两边空格后读入到一个list中
        for line in f.readlines():
            line_list.append(line)
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

#用指定内容匹配文件中的每一行
def match(line,content):
    res=line.find(content)
    return res
#把列表中的内容写到文件中
def list_write_into_file(li):
    with open(file_name,'w') as new_file:
        for xx in li:
            new_file.write(xx)

#返回文件list每行的匹配值的list
def return_search_list(readlines_list,user_input):
    readlines_list_return=[]
    for aaa in readlines_list:
        b=aaa.find(user_input)
        readlines_list_return.append(b)
    return readlines_list_return

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
    while True:
        user_input=input('请输入您要查找的域名：')
        read_list=file_read_to_list()
        search=return_search_list(file_read_to_list(),user_input)
        for ii in search:
            if ii==-1:
                continue
        else:
            print('您查找的记录不存在')
            function_list()


def modify():
    pass

def add():
    while True:
        user_input=input('请输入修改内容，注意使用双引号，（提示：‘{"backend": "test.oldboy.org","record":{"server": "100.1.7.999","weight": 20,"maxconn": 30}}’）').strip()
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
            backend='backend %s'%domain
            record='server {0} {1} weight {2} maxconn {3}'.format(server_ip,server_ip,weight,maxconn)

            #在文件list下所有的元素中匹配域名，域名不在的情况下
            res_list=return_search_list(new_line_list,backend)
            for i in res_list:
                if i==-1:
                    continue
                else:
                    i_index=new_line_list.index(backend+'\n')#如果i不等于-1，说明域名已经存在文件中，记录i的索引,i的索引等于backen在文件list中的索引
                    #i_index+1开始到文件结尾生成一个心的临时列表，在这个列表中循环，如果文件的开始不以server开头，记录这个索引的位置，再生成一个临时列表，
                    hava_find_domain_list=new_line_list[i_index+1:]
                    for start in hava_find_domain_list:
                        #如果line不以server开头，记录的index
                        if str(start).strip().startswith('server') or str(start).strip()=='\n' or len(str(start))==0:
                            continue
                        else:
                            end_index=hava_find_domain_list.index(start)
                            start_list=new_line_list[i_index+1:i_index+1+end_index]#
                            start_strip_list=[]
                            for item in start_list:
                                start_strip_list.append(str(item).strip().strip('\n'))
                            if record in start_strip_list:
                                print('您要添加的记录已经存在，无法添加！！')
                                function_list()
                            else:
                                new_line_list.insert(i_index+1,' '*8+record+'\n')
                                list_write_into_file(new_line_list)
                                print('域名存在，在文件中间添加记录成功')
                                function_list()
                    else:
                        new_line_list.insert(i_index+1,' '*8+record)
                        list_write_into_file(new_line_list)
                        print('域名存在，在文件末尾添加记录成功')
                        function_list()

            else:
                #如果res_list中所有的元素都等于-1，说明域名不在文件列表中

                file_append('\n'+backend+'\n')
                file_append(' '*8+record+'\n')
                print('新添加记录成功')

def delete():
    pass

if  __name__ == '__main__':
    while True:
        function_list()



