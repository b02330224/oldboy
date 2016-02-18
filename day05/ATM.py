#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
__author__='weiqiang'
blog:http://www.cnblogs.com/weiqiangwang/
'''

import sys,json

ATM_info='ATM_info.json'

#读出ATM信息
def read_out_ATM():
    with open(ATM_info,'r')as f:
        return json.load(f)

#更新ATM信息
def update_ATM_info(data):
    with open(ATM_info,'w') as f:
        json.dump(data,f)


#信用卡验证
def card_auth(cardID,passwd):
    card_info=read_out_ATM()
    for i in card_info:
        if i==cardID and card_info[i]['draw_passwd']==passwd:
            return True
        else:
            continue
    else:
        print('卡号或者密码错误')
        return False
#查询指定信用卡的信息
def quary_card_info(cardID):
    all_card_info=read_out_ATM()
    return all_card_info[cardID]

#查询指定的信用卡是否存在
def if_card_ok(cardID):
    all_card_info=read_out_ATM()
    if cardID in all_card_info:
        return True
    else:
        print('您输入的卡号不存在')
        return False

#更新指定信用卡卡的信息
def update_card_info(cardID,card_info):
    all_info=read_out_ATM()
    for i in all_info:
        if i==cardID:
            all_info[i]=card_info
        else:
            continue
    return update_ATM_info(all_info)

#申请信用卡
def add_card(cardID,passwd,edu=15000,remain_edu=15000):
    all_card_info=read_out_ATM()
    if  cardID not in all_card_info:
        all_card_info[cardID]={'draw_passwd':passwd,'edu':edu,'remain_edu':remain_edu}
        update_ATM_info(all_card_info)
        return True
    else:
        print('您所添加的卡号已存在，添加失败！')
        return False

#注销信用卡(需要验证卡号密码)
def del_card(cardID,passwd):
    all_card_info=read_out_ATM()
    for i in all_card_info:
        if i==cardID:
            if card_auth(cardID,passwd):
                del_card=all_card_info.pop(i)
                print('卡号为%s 的信用卡已被注销'%del_card)
                return True
        else:
            continue
    print('删除的卡号不存在')
    return False
#转账
def tran_money(from_card,to_card,tran_sum):
    from_card_info=quary_card_info(from_card)
    to_card_info=quary_card_info(to_card)
    from_card_info['remain_money']-=int(tran_sum)
    to_card_info['remain_money']+=int(tran_sum)
    update_card_info(from_card,from_card_info)
    update_card_info(to_card,to_card_info)

def check_input(type):
    try:
        int(type)
        return 1
    except:
        return 0

#信用卡为类
class card1(object):
    def __init__(self,cardID,passwd):
        self.cardID=cardID
        self.passwd=passwd

    def quary_money(self):
        remain_money=quary_card_info(self.cardID)['remain_money']
        edu=quary_card_info(self.cardID)['edu']
        print('您的账户额度为%s'%edu)
        print('您的可用额度为%s'%remain_money)

    #转账(转账需要)
    def money_tran(self):
        remain_money=quary_card_info(self.cardID)['remain_money']
        print('您当前账户余额为%s'%remain_money)
        while True:
            to_card=input('请输入您的转入卡号')
            if  if_card_ok(to_card):
                while True:
                    tran_sum=input('请输入您的转账金额')
                    if remain_money>=int(tran_sum):
                        tran_money(self.cardID,to_card,tran_sum)
                        print('转账成功')
                        menu(self)
                    else:
                        print('余额不足,请重新输入转账金额或者（M）返回主菜单')
                        if tran_sum=='M':
                            menu(self)
            else:
                print('您输入的卡号有误，请重新输入')
    #账户管理
    def account_manage(self,cardID,passwd,edu,remain_money):
        print('申请信用卡（A）  注销信用卡（D）')
        while True:
            user_input=input('请输入您的选择：')
            if user_input=='A' or user_input=='a':
                cardID=input('请输入您喜欢的信用卡号：')
                while True:
                    passwd=input('请设置信用卡密码')
                    second_passwd=input('请再确认一次：')
                    if passwd==second_passwd:
                        add_card(cardID,passwd)
                        print('信用卡申请成功')
                    else:
                        print('两次密码输入不一致，请重新设置')
            elif user_input=='D' or user_input=='d':
                del_card(cardID.passwd)


#ATM功能菜单
def menu(card):
    print('(1)转账'.ljust(40))
    print('(2)查账'.ljust(40))
    print('(3)账户管理'.ljust(40))
    print('(4)取现'.ljust(40))
    print('(5)查看操作记录'.ljust(40))
    print('(6)返回商城主菜单')
    while True:
        print('*'*40)
        chioce=input('请选择功能清单编号：')
        res=check_input(chioce)
        if res==0:
            print('请选择列表中的标号')
            continue
        elif chioce=='1':card.money_tran()
        elif chioce=='2':card.quary_money()
        elif chioce=='3':card.account_manage()
        elif chioce=='4':print('还没开发')
        elif chioce=='5':print('还没开发')
        elif chioce=='6':sys.exit(0)

def ATM_login():
    while True:
        cardID=input('请输入您的卡号：')
        card_passwd=input('请输入您的密码:')
        all_card_info=read_out_ATM()
        for i in all_card_info:
            if i==cardID and all_card_info[i]['draw_passwd']==card_passwd:
                card=card1(cardID,card_passwd)
                menu(card)
            else:
                print('您输入的帐号或者密码有误')




