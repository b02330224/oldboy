#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
__author__='weiqiang'
blog:http://www.cnblogs.com/weiqiangwang/
'''
import json,sys

#持久化商品信息
def write_into_shangpin(shangpin):
    with open('shangpin.json','w') as f:
        json.dump(shangpin,f)

#write_to_file(shangpin)

#加载商品信息
def read_out_shangpin():
    with open('shangpin.json','r') as z:
        return json.load(z)


#持久化用户信息文件
def write_into_userinfo(info_list):
    with open('user.json','w') as x:
        json.dump(info_list,x)
#write_to_shangpin(info_list)

#加载用户信息
def read_out_userinfo():
    with open('user.json','r') as c:
        return json.load(c)
#持久化购车车信息
def write_into_gouwuche(gouwu):
    with open('gouwuche.json','w') as m:
        json.dump(gouwu,m)

#加载购物车信息
def read_out_gouwuche():
    with open('gouwuche.json','r') as v:
        return json.load(v)

#加载银行卡信息
def read_out_ATM():
    with open('ATM_info.json','r') as mm:
        return json.load(mm)

#检查购物车是否为空
def check_gouwuche_empty(input_name):
    try:
        if read_out_gouwuche().has_key(input_name):
            return 1
        else:
            return 0
    except:
        with open('gouwuche.json','w')as vv:
            xxx={}
            json.dump(xxx,vv)

#检查输入是否为数字
def check_input(type):
    try:
        int(type)
    except:
        return 1
############################################################################################################
def login():
    #加载用户信息
    user_info=read_out_userinfo()

    print(user_info)#测试用

    while True:
        global input_name
        flag=False
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
                        show_chioce()#进入功能菜单
                        flag=True
                        return flag

                    else:
                        passwd_try_times -= 1
                        if passwd_try_times> 0:
                            print('你还有%s次机会'%passwd_try_times)
                 #如果剩余重试密码次数为0，改变用户状态为locked，同时持久化用户信息并退出！
                else:
                    user_info[input_name]['status']='locked'
                    write_into_userinfo(user_info)
                    print('输入密码错误次数太多，已被锁定，强制退出')
                    sys.exit(1)
#####################################################################################################################
#手机购买菜单
all_user_gouwu_list={}
def show_menu():
    if check_gouwuche_empty(input_name):
        gouwu_list=read_out_gouwuche()[input_name]
    else:
        all_user_gouwu_list[input_name]={}
        gouwu_list=all_user_gouwu_list[input_name]

    while True:
        n=1
        num_dict={}
        shangpin=read_out_shangpin()
        info_user=read_out_userinfo()

        print('商品编号'.center(20),'商品名称'.center(15),'商品价格'.center(30),'商品数量'.center(1))
        for i in shangpin.keys():#生成编号和商品对应的字典
            price=shangpin[i]['price']
            num=shangpin[i]['num']
            print('   ',str(n).center(20),'   ',i.ljust(30),str(price).ljust(5),'   ',str(num).center(25))
            num_dict[n]=i
            n+=1
        input_num=input('请输入您想要购买的手机编号（b）返回功能菜单：')
        if input_num=='b':
            show_chioce()
        elif check_input(input_num) ==1:
            print('请输入数字')
        elif int(input_num) not in num_dict.keys():
            print('请输入正确的手机编号')
        else:
            choiced_shangpin=num_dict[int(input_num)]#选择的商品
            shangpin_num=shangpin[choiced_shangpin]['num']#商城中的商品数量
            #如果商品数量大于0
            if shangpin_num >0:
                if choiced_shangpin in gouwu_list.keys():
                    gouwu_list_num=gouwu_list[choiced_shangpin]['num']#购物车中的商品数量
                    gouwu_list_num+=1#购物车数量增加
                    shangpin_num-=1#商城中的商品数量扣除'
                    shangpin[choiced_shangpin]['num']=shangpin_num#商品信息更新
                    gouwu_list[choiced_shangpin]['num']=gouwu_list_num#购物车信息更新
                    all_user_gouwu_list[input_name]=gouwu_list#更新总的购物车字典

                else:
                    gouwu_list[choiced_shangpin]={'num':int(1)}#没有此种商品时，添加购物车
                    shangpin_num-=1#商城中的商品数量减一
                    shangpin[choiced_shangpin]['num']=shangpin_num#商城中的商品数量进行更新
                    all_user_gouwu_list[input_name]=gouwu_list#更新购物车
            else:
                print('此商品已经卖光了，下次早点儿来！！！')
            #持久化数据
            write_into_gouwuche(all_user_gouwu_list)
            write_into_shangpin(shangpin)
            print('您已经购买如下商品：')
            print('商品名称','商品数量')
            #提示用户购物车中的商品
            for shangpin_name in read_out_gouwuche()[input_name].keys():
                print(shangpin_name,str(gouwu_list[shangpin_name]['num']))
            #购物提示
            while True:
                con_input=input('继续购物(c),(p)结账，返回功能菜单（b）:')
                if con_input=='c':
                    break
                elif con_input=='b':
                    show_chioce()
                elif con_input=='p':
                    settle_account()
                else:
                    print('请按提示输入')

 ################################################################################################################
#结账
def settle_account():
    user_info=read_out_userinfo()
    if user_info[input_name].has_key('cardID'):
        cardID=user_info[input_name]['cardID']
        if check_gouwuche_empty(input_name):#检查购物车是否为空
            ATM_list=read_out_ATM()
            remain_money=read_out_ATM[cardID]['keyongedu']
            goods_list=read_out_gouwuche()[input_name]

            cost=0
            for good in goods_list.keys():
                cost+=read_out_shangpin()[good]['price']*goods_list['num']
            if remain_money>cost:
                yu=remain_money-cost
                print('结算成功，您的余额为%d元'%yu)
                ATM_list[cardID]['keyongedu']=yu#更新ATM字典信息

            else:
                print('您的余额不足，请充值或者修改您的购物车')
                show_chioce()
        else:
            print('您尚未购买任何商品，请到商城买!')
            show_menu()
    else:
        print('您还未绑定银行卡，请先去绑定卡片,自动为您返回主菜单')
        show_chioce()

'''
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

'''

###############################################################################################
#查询余额
def show_remain(user):
    with open('user.json','r') as d:
        user_list=json.load(d)
        print('您当前账户余额为%d'%user_list[user]['remain'])
    show_chioce()

#查询购物车
def show_gouwu(input_name):
    while True:
        try:
            gouwuche_list=read_out_gouwuche()[input_name]
        except:
            print('您还未购买商品，请您到购买菜单选择商品')
            show_menu()
            break

        print('已经购买如下商品\n')
        for ii in gouwuche_list:
            print(ii,gouwuche_list[ii]['num'])
        while True:
            cont_input=input('继续购物(c),结账（s）,返回功能菜单（b）:')
            if cont_input=='c':
                show_menu()
            elif cont_input=='b':
                show_chioce()
            elif cont_input=='s':
                settle_account()
            else:
                print('请按提示输入')

########################################################################################
#功能菜单
def show_chioce():
    print('欢迎来到手机商城'.center(60,'*'))
    print('(1)进入手机购买菜单')
    print('(2)查看购物车清单')
    print('(3)结算系统')
    print('(4)退出系统')
    print('*'*60)
    while True:
        chioce=input('请选择功能清单编号：')
        res=check_input(chioce)
        if res==1:
            print('请选择列表中的标号')
            continue
        elif chioce=='1':show_menu()
        elif chioce=='2':show_gouwu(input_name)
        elif chioce=='3':settle_account()
        elif chioce=='4':sys.exit(0)
        else:continue
############################################################################################################



if __name__ == '__main__':
    if login():
        show_chioce()







