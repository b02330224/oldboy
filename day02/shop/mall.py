#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
__author__='weiqiang'
blog:http://www.cnblogs.com/weiqiangwang/
'''
'''
import json
info_list={'aaa':{'passwd':'123456','status':'unlocked','remain':int(0)},'bbb':{'passwd':'123456','status':'unlocked','remain':int(0)}}
def checkout(info_list):
    with open('user.json','w') as x:
        json.dump(info_list,x)
checkout(info_list)


'''
import json
import sys
import getpass
#import login

#shangpin={'iphone7':{'num':int(2),'price':int(6000)},'iphone6':{'num':int(3),'price':int(4600)},'xiomi4':{'num':int(5),'price':int(1800)},'letv':{'num':int(3),'price':int(2600),},'qiku':{'num':int(2),'price':int(1300)}}

#info_list={'aaa':{'passwd':'123456','status':'unlocked','remain':int(0)},'bbb':{'passwd':'123456','status':'unlocked','remain':int(0)}}



#持久化商品信息
def write_to_file(shangpin):
    with open('shangpin.json','w') as f:
        json.dump(shangpin,f)
#write_to_file(shangpin)


#加载商品信息
def read_out():
    with open('shangpin.json','r') as z:
        json.load(z)


############################################################################################################
def login():

#持久化用户信息文件
    def checkout(info_list):
        with open('user.json','w') as x:
            json.dump(info_list,x)
    #checkout(info_list)

    #加载用户信息
    def checkin():
        with open('user.json','r') as c:
            return json.load(c)

    user_info=checkin()
    print(user_info)#测试用

    while True:
        global input_name
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
                    input_passwd=input('请输入您的密码：')
                    if input_passwd == user_info[input_name]['passwd']:  #如果用户名和密码对应
                        print('恭喜你登录成功！')
                        show_chioce()

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
#####################################################################################################################
#手机购买菜单
def show_menu():
    gouwu_list={}
    while True:
        n=1
        num_dict={}
        with open('shangpin.json','r') as y:
            shangpin=json.load(y)
        with open('user.json','r') as l:
            info_user=json.load(l)

        print('商品编号'.center(20),'商品名称'.center(15),'商品价格'.center(30),'商品数量'.center(1))
        for i in shangpin.keys():
            price=shangpin[i]['price']
            num=shangpin[i]['num']
            print('   ',str(n).center(20),'   ',i.ljust(30),str(price).ljust(5),'   ',str(num).center(25))
            n+=1
            num_dict[n]=i
        input_num=input('请输入您想要购买的手机编号（b）返回功能菜单：')
        if input_num=='b':
            show_chioce()
        elif check_input(input_num) ==1:
            print('请输入数字')
        elif input_num not in num_dict.keys():
            print('请输入正确的手机编号')
        else:
            choiced_shangpin=num_dict[int(input_num)]
            shangpin_num=shangpin[choiced_shangpin]['num']
            for shouji in shangpin.keys():
                price_list=[]
                price_list.append(shangpin[shouji]['price'])
            min_price=min(price_list)
            if shangpin_num >0 and info_user[input_name]['price']>min_price:
                if choiced_shangpin in gouwu_list:
                    gouwu_list[choiced_shangpin]['num']+1
                    shangpin_num-=1
                else:
                    gouwu_list[choiced_shangpin]={}
                    gouwu_list[choiced_shangpin]['num']=1
                    shangpin_num-=1
            else:
                if shangpin_num ==0:
                    print('此商品已经卖光了，下次早点儿来！！！')
                else:
                    print('您的余额已不足，请充值后再购买')
            write_to_file(shangpin)
            print('您已经购买如下商品：')
            print('商品名称','商品数量')
            for shangpin_name in gouwu_list:
                print(shangpin_name,gouwu_list[shangpin_name['num']])





 ################################################################################################################

#充值函数
def recharge(user):
    while True:
        rechare_money=input('请输入你的充值金额,(b)返回功能菜单：')
        re=check_input(rechare_money)
        if rechare_money=='b':
            show_chioce()
        elif re==1:
            print('请输入数字！！！！！')
        else:
            with open('user.json','r') as e:
                info_list=json.load(e)
                remain=info_list[user]['remain']+int(rechare_money)
                info_list[user]['remain']=remain
                print('您当前的余额为%d'%info_list[user]['remain'])
            with open('user.json','w')as m:
                json.dump(info_list,m)



###############################################################################################
#功能菜单
def show_chioce():
    print('*'*60)
    print('(1)进入手机购买菜单')
    print('(2)给账户充值')
    print('(3)查看账户余额')
    print('(4)退出系统')
    print('*'*60)
    while True:
        chioce=input('请选择功能清单编号：')
        res=check_input(chioce)
        if res==1:
            print('请选择列表中的标号')
            continue
        elif chioce=='1':show_menu()
        elif chioce=='2':recharge(input_name)
        elif chioce=='3':show_remain(input_name)
        elif chioce=='4':sys.exit(0)
        else:continue
############################################################################################################
#显示余额
def show_remain(user):
    with open('user.json','r') as d:
        user_list=json.load(d)
        print('您当前账户余额为%d'%user_list[user]['remain'])


#检查输入是否为数字
def check_input(type):
    try:
        int(type)
    except:
        return 1


def main():
    login()

if __name__ == '__main__':
    main()







