#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
__author__='weiqiang'
blog:http://www.cnblogs.com/weiqiangwang/
'''
import time
import sys
import random

#实现间隔时间输出
def interval_print(print_content):
    for i in print_content:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.3)

#检查是否为数字
def check_num(user_input):
    try:
        int(user_input)
        return 1
    except:
        print('请输入数字')
        return 0
class xiaoming_roles(object):
    def __init__(self,name,age,work,salary):
        self.name=name
        self.age=age
        self.work=work
        self.salary=salary

def menu():
    print('''
        你现在可以去搞对象了！！！
        ''')
    xiaofang_name=input('请输入你想和谁搞。。。对象')
    xiaofang=xiaofang_name
    print('''
    你可以带%s进行以下项目：
    1、请%s吃一顿
    2、去希腊爱琴海甜蜜之旅
    3、去打工
    ''')



    def train(self):
        while True:
            print('''
            你可以学习以下课程：
            1、Linux中高级运维
            2、mysql DBA
            3、java
            4、python
            5、Linux架构师
            ''')
            tranin_class=input('请输入您要需要学的课程编号：')
            if tranin_class=='1':
                self.salary=10000
                interval_print('正在学习Linux中高级课程...1个月...2个月...4个yue，你的工资现在是10000')
                break
            elif tranin_class=='2':
                self.salary=12000
                interval_print('正在学习mysql DBA...1个月...2个月...4个yue，你的工资现在是12000')
                break
            elif tranin_class=='3':
                self.salary=10000
                interval_print('正在学习JAVA...1个月...2个月...4个yue，你的工资现在是10000')
                break
            elif tranin_class=='4':
                self.salary=25000
                interval_print('正在学习PYTHON...1个月...2个月...4个yue，你的工资现在是25000')
                break
            elif tranin_class=='5':
                self.salary=18000
                interval_print('正在学习Linux架构师...1个月...2个月...4个yue，你的工资现在是18000')
                break
            else:
                print('请输入正确的选项')
        def chifan():
            while True:
                print('''
                请选择套餐：
                1、黄焖鸡米饭
                2、小鸡炖蘑菇
                3、满汉全席
                ''')
                chifan_input=input('请点餐：')
                








class xiaofang(object):
    def __init__(self,name,xingfenzhi):
        self.xinfenzhi=xingfenzhi
        self.xinfenzhi=100



xiaoming_name=input('请输入你的名字：')
while True:
    xiaoming_salary=input('请输入你的工资:')
    if check_num(xiaoming_salary):
        xiaoming=xiaoming_roles(xiaoming_name,xiaoming_salary)
        if int(xiaoming.salary)<=5000:
            interval_print('屌丝，赶紧去老男孩培训变身高富帅吧！！！')
            print('''\n
            1、去培训
            2、我就不去
            ''')
            while True:
                user_choice=input('请输入您的选择：')
                if user_choice=='1':
                    xiaoming.train()
                elif user_choice=='2':
                    print('你这辈子注定是一个屌丝了，你搞不了对象了！！！回家种地去吧！拜拜！！')
                    sys.exit(0)
                else:
                    print('您的输入有误！！！')




