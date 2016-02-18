#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
__author__='weiqiang'
blog:http://www.cnblogs.com/weiqiangwang/
'''
import json
import sys
import getpass

#import login

shangpin={'iphone7':{'num':int(5),'price':int(6000)},
          'iphone6':{'num':int(5),'price':int(4600)},
          'xiomi4':{'num':int(5),'price':int(1800)},
          'letv':{'num':int(5),'price':int(2600),},
          'qiku':{'num':int(5),'price':int(1300)}}

user_info={'aaa':{'passwd':'123456','status':'unlocked','cardID':['100']},
           'bbb':{'passwd':'123456','status':'unlocked','cardID':['101']}}

ATM_info={'100':{'draw_passwd':'100',
                 'edu':int(20000),
                 'remain_money':int(20000)
                 },
          '101':{'draw_passwd':'101',
                 'edu':int(20000),
                 'remain_money':int(20000)
                 }
          }
#持久化商品信息
def write_into_shangpin(shangpin):
    with open('shangpin.json','w') as f:
        json.dump(shangpin,f)


#持久化用户信息文件
def write_into_userinfo(info_list):
    with open('user.json','w') as x:
        json.dump(info_list,x)

#持久化ATM信息
def write_into_ATM(ATM_info):
    with open('ATM_info.json','w') as xx:
        json.dump(ATM_info,xx)

write_into_shangpin(shangpin)
write_into_userinfo(user_info)
write_into_ATM(ATM_info)
