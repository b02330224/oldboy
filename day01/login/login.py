#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import json
import getpass


#调试用
#info_list={'aaa':{'passwd':'123456','status':'locked'},'bbb':{'passwd':'123456','status':'unlocked'}}

#持久化用户信息文件
def checkout(info_list):
    with open('info.json','w') as f:
        json.dump(info_list,f)
#checkout(info_list)

#加载用户信息
def checkin():
    with open('info.json','r') as f:
        return json.load(f)

user_info=checkin()
print(user_info)

while True:
    input_name=input('输入您的用户名：')
    #如果用户名不在字典中
    if input_name not in user_info:
        print('用户名不存在，请重新输入！')
    else:
        if user_info[input_name]['status']== 'locked':#如果用户名是锁定状态
            print('你的用户名已经被锁定，请24小时后再试!')
        else:
            passwd_try_times = 3
            while passwd_try_times>0:
                input_passwd=getpass.getpass(prompt='请输入您的密码：')
                if input_passwd == user_info[input_name]['passwd']:  #如果用户名和密码对应
                    print('恭喜你登录成功！')
                    sys.exit(0)
                else:
                    passwd_try_times -= 1
                    if passwd_try_times> 0:
                        print('你还有%s次机会'%passwd_try_times)
             #如果剩余重试密码次数为0，改变用户状态为locked，同时持久化用户信息并退出！
            else:
                user_info[input_name]['status']='locked'
                checkout(user_info)
                print('输入密码错误次数太多，已被锁定，强制退出')
                sys.exit(1)



