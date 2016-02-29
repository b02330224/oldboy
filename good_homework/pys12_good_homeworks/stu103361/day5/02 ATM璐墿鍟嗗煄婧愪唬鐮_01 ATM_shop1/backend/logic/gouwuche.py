__author__ = 'Administrator'
#-*- coding:utf-8 -*-
import json
import time
import datetime
import socket
import sys
# print(sys.path) #默认路径是当前py文件的父目录

from backend.db.sql_api import select
# from backend.db import json2
#from 模块 import 方法名字（函数名字）

ipaddr = socket.gethostbyname(socket.gethostname())  #记录登录ip，定义成全局变量

#登录接口已经用json重写
def Login(username):  #登录接口需要传入main函数的32行，输入的用户名作为实参传递过来
    #1 json读出字典--文件中以字典的形式存储数据
    q_data_login = select("username","bbb")
    # print(q_data_login)  #{'jack': {'times': 0, 'pwd': 123}, 'tom': {'times': 0, 'pwd': 123}}

    #2逻辑判断--字典中修改错误登录次数
    while True: #判断用户名，外循环，用于输入用户名
        # username = input("请输入用户名:")  #登录接口需要传入main函数的32行，输入的用户名作为实参传递过来，这里就不另外输入的
        if len(username) == 0:  #判断用户名是否正确
            print("\033[31;1m用户名不能为空\033[0m")
        elif username not in q_data_login:
            print("\033[31;1m用户名不存在\033[0m")
        else:
            if q_data_login[username]["times"] >= 3 :  #判断错误登录次数是否大于等于3
                print("\033[31;1m账号锁定，请联系管理员\033[0m")
                break
            else:
                while True: #内循环，用于输入密码
                    passwd = int(input("请输入密码:"))  #这里输入的是字符串，文件中的密码是整数123的形式，所有转换成int，也可以把文件中的123变成"123"
                    if passwd == q_data_login[username]["pwd"]:
                        q_data_login[username]["times"] =0
                        print("\033[32;1m登录成功\033[0m",username)
                        break_flag = True
                        # break  #跳出内循环
                        return  #这里返回的是None，计算器函数可以正常执行--162行
                    else: #密码不对，但是错误登录次数<3
                        q_data_login[username]["times"] += 1
                        times = q_data_login[username]["times"]
                        left_times = 3- times
                        if left_times ==0:
                            print("\033[31;1m账号锁定，请联系管理员\033[0m")
                            break_flag = True
                            break #跳出内循环
                            # return "\033[31;1m账号锁定，请联系管理员1\033[0m" #这里返回的不是None，162行函数return终止了，计算器函数就不执行了
                        else:
                            print("\033[31;1m密码输入错误，请重新输入，您还有 %s 次输入机会，3次密码输入错误，账号锁定" \
                                  "密码输入正确后，错误登录次数重置为0\033[0m" % (left_times))
                            continue #跳出内循环当次迭代
                if break_flag:  #跳出外循环，和39行while同一级
                    break  #跳出外循环

    #3将修改后的错误登录次数写入文件
    f = open("username1.txt","w") #新建一个新文件
    json.dump(q_data_login,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_mima转换后写入f）
    f.close()

def Errorhandle(): #执行功能函数后，处理错误或者提示错误
    print('after:购物商城使用前，需要登录，使用后的收尾工作，留作后续扩展，敬请期待')   # #相当于在查看tv页面后，执行收尾工作（例如退出用户名登录）

#2默认装饰器（框架）--一个函数被多个装饰器装饰（这里不必写2个装饰器，只需要写2个函数即可，4,7行）
def Filter(before_func,after_func):
    def outer(main_func):  #func=tv
        def inner(*args,**kwargs):  #inner() = tv()  15行，装饰器的前置函数呆了参数，这里inner就加了*args,**kwargs
            # print("用户名密码验证")   #用户名密码验证功能-函数
            # func(request,kargs)   #func() = tv()   #执行tv查看函数  15行
            before_result = before_func(*args,**kwargs)  #登录密码验证
            if(before_result != None):  #登录有return，说明登录失败，自己定义的，功能函数不执行
                return before_result;    #返回登录错误信息

            main_result = main_func(*args,**kwargs)  #业务函数 index
            if(main_result != None):  #业务函数有return，说明业务函数失败，自己定义的，功能函数不执行
                return main_result;   #返回业务函数错误信息

            after_result = after_func()  #收尾函数
            if(after_result != None): ##执行业务函数后，处理一些收尾工作
                return after_result;   #返回收尾函数错误信息
        return inner   #inner = tv
    return outer

#一商城函数
#1处理用户输入的字典,将字典的key处理成已经排序的列表，用于拼接字符串
def chushihua(arg1):  #arg1是形式参数  主模块mydic是实际参数传入（调用函数的时候，传入实参）
    li_dickey=arg1.keys()   #将用户输入的字典的key添加到列表，无序的，无法通过索引号定位
    li_dickey = list(li_dickey)  #字典的key需要转换成list，才能排序
    li_dickey.sort()   #将列表排序后，通过索引号取出字典的key
    return li_dickey   #返回已经排序的列表

@Filter(Login, Errorhandle)
#修改购买数量和用户余额
def home(user):#支付接口  这里形参user，对应的实参是主函数的jack，tom（用户输入的）
    total =0 #定义商品一共多少钱
    q_data = select("shop","ddd")  #1读商品表
    # print(q_data)  #{'1': {'price': 6099, 'goods': 'iphone6s', 'times': 0}, '2': {'price': 8888, 'goods': 'mac', 'times': 0}}
    q_data_yue = select("yue","ddd") #2读用户余额表
    # print(q_data_yue) #{'jack': {'yue': 15000, 'yusuan': 15000}}
    num = q_data_yue[user]["yusuan"]   #定义购物预算（兜里一共多少钱） 预算可以直接定义，也可以从文件中读取
    yue = q_data_yue[user]["yue"]  #用户的余额
    break_flag = False  #跳出外循环标识

    ret = chushihua(q_data[user]) #将字典的键放在列表中，给列表排序
    q_data[user][ret[0]]["times"] = 0 #每次购买前，先将购买数量置为0
    q_data[user][ret[1]]["times"] = 0 #如果不将购买数量置为0，就是个累计效应

    #3修改购买数量和余额
    while True: #外循环，输入商品编号
        print("----欢迎购物----")
        print("---商品编号列表---")
        print ('%-7s%-7s%-7s%-7s' % ("商品编号", "商品名称","商品价格", "购买数量"))
        print ('%-11s%-11s%-11s%-11s' % (ret[0], q_data[user][ret[0]]["goods"],q_data[user][ret[0]]["price"], q_data[user][ret[0]]["times"]))
        print ('%-11s%-11s%-11s%-11s' % (ret[1], q_data[user][ret[1]]["goods"],q_data[user][ret[1]]["price"], q_data[user][ret[1]]["times"]))
        # #打印商品编号列表
        print("您的余额目前是%s元" % q_data_yue[user]["yue"])
        yue_before = q_data_yue[user]["yue"]
        goods_no_input = input("请输入你要买的商品编号:") #要求用户输入商品编号
        if len(goods_no_input)==0: #如果商品编号为空
            print("\033[31;1m商品编号不能为空\033[0m")
        elif goods_no_input not in q_data[user]: #如果商品编号不存在
            print("\033[31;1m商品编号不存在\033[0m")
        else: #商品编号存在(调支付接口),下面的支付结算单独成一个函数，支付密码验证用装饰器
            # print("1",total)
            if  total < num and yue>q_data[user][goods_no_input]["price"]: #bug修复，当商品总价格超过用户预算的时候，就不要再累加商品价格了，否则会出现98行，余额是负数的情况
                total += q_data[user][goods_no_input]["price"]  #累加商品的价格（需要支付多少钱）
            # print("2",total)
            # # 先计算商品总价格，在将商品这价格和预算比对
            if total < num and yue>q_data[user][goods_no_input]["price"]: #如果需要支付的钱小于用户的预算
                q_data[user][goods_no_input]["times"] += 1  #购买数量+1
                # print("3",q_data_yue["jack"]["yue"])
                # q_data_yue["jack"]["yue"] -= total
                q_data_yue[user]["yue"] -= q_data[user][goods_no_input]["price"]    #关键点：原始的余额是10000文件中，每买一件商品，余额扣减商品的价格
                #这里必须将total改成shop_dict[goods_no_input]["price"]  否则逻辑不对
                # print("4",q_data_yue["jack"]["yue"])
                # yue_list[-1] = num - total   #用户预算扣除购物车的花费后，计算用户的余额
                # print("已经放入购物车，输入x，继续购物；输入y，去结算，请输入支付密码结算")
                while True:
                    jiesuan = input("输入y，去结算；输入a，继续购买:")
                    if jiesuan == "y":
                        login(user)  #调支付密码验证函数,这里需要将注册后输入的用户名作为参数传入
                        break  #跳出循环的当前迭代，回到75行
                    elif jiesuan == "a":
                        # break_flag = True  #外循环跳出标签
                        break
                    else:  #如果输入的不是x或者y
                        print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
                        continue  #跳出内循环本次迭代

                print("\033[32;1m目前没有超出预算，当前余额是%s元,可以继续购买,输入c，退出程序；输入a，继续购买:\033[0m:" % q_data_yue[user]["yue"])
                while True:
                    tuichu1 = input("确认退出程序么？输入c，退出程序；输入a，继续购买:")
                    if tuichu1 == "a":
                        break  #跳出循环的当前迭代，回到75行
                    elif tuichu1 == "c":
                        break_flag = True  #外循环跳出标签
                        break
                    else:  #如果输入的不是a或者c
                        print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
                        continue  #跳出内循环本次迭代
                        # print total
                if break_flag:
                    break  #跳出外循环
            if total >= num or yue<q_data[user][goods_no_input]["price"] : #如果需要支付的钱大于等于用户的预算，钱不够了，计算用户余额和用户买这个商品还差多少钱
                cha_money = total - num #商品总价格-用户预算=用户差的钱
                # yue_list[-1] = shop_dict[goods_no_input]["price"]-cha_money
            #如果left_money为负数，取绝对值（用户差的钱+用户的余额=商品的价格）
                print("\033[31;1m钱不够了,当前余额是%s元，想要买这件商品，还差%s元\033[0m" % (q_data_yue[user]["yue"],q_data[user][goods_no_input]["price"]-yue))

                while True:#定义内循环，判断退出
                    tuichu = input("确认退出程序么？输入q，退出程序；输入b，返回上一级菜单；输入c，给用户充值:")
                    if tuichu == "q":  #
                        print("\033[32;1m退出程序,打印购物单如下：\033[0m")
                        break_flag = True  #外循环退出标识
                        break  #跳出循环
                    elif tuichu == "b":
                        total -= q_data[user][goods_no_input]["price"]
                        #bug修复，返回上一级的时候，最后一个商品由于预算不够，所以必须要扣减最后一个商品的价格
                        # print total
                        print("\033[32;1m返回上一级菜单,请重新输入你要买的商品编号:\033[0m")
                        break #跳出内循环本次迭代
                        # continue
                    elif tuichu == "c":
                        pass
                        # chongzhi.txt()
                    else:  #如果输入的不是q或者b
                        print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
                        continue  #跳出内循环本次迭代
                if break_flag:
                    break  #跳出外循环

    f = open("shop.txt","w") #新建一个新文件
    # f.seek(0)  #回到文件最开始
    json.dump(q_data,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data转换后写入f）
    f.close()

    #5修改后的余额写文件
    f = open("username1.txt","w") #新建一个新文件
    # f.seek(0)
    json.dump(q_data_yue,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_yue转换后写入f）
    f.close()

    #5打印购物清单和余额（累计）
    print("---购物清单---")
    print ('%-7s%-7s%-7s%-7s%-7s' % ("商品编号", "商品名称","商品价格", "购买数量","购买用户"))
    print ('%-11s%-11s%-11s%-11s%-11s' % (ret[0], q_data[user][ret[0]]["goods"],q_data[user][ret[0]]["price"], q_data[user][ret[0]]["times"],user))
    print ('%-11s%-11s%-11s%-11s%-11s' % (ret[1], q_data[user][ret[1]]["goods"],q_data[user][ret[1]]["price"], q_data[user][ret[1]]["times"],user))
    print("您的余额目前是%s元" % q_data_yue[user]["yue"])
    yue_after = q_data_yue[user]["yue"]

    #6购物结算后，新建一个历史记录表
        #构造字典，往字典添加键值对，写入到文件
    my_dic1 = {'name':user,"ipaddr":ipaddr, 'money': yue_before-yue_after,"type":"gouwu","time":time.strftime('%Y-%m-%d %H:%M:%S')}
    # print(my_dic1)

    j_str = json.dumps(my_dic1)  #先把字典转换成字符串
    f = open("gouwu_his.txt","a")  #往原有的文件中追加取款记录
    f.write(j_str)   #再写入到文件
    f.write("\n")   #添加换行符  这里手动添加换行
    # f.write(data) #直接写入字典，报错 TypeError: write() argument must be str, not dict
    f.close()

    #7打印单次购物记录-时间 地点 人物 事件（每次购物结算时花了多少）
    print("---购物历史记录---")
    print ('%-20s%-20s%-9s%-9s%-9s' % ("时间","登录IP", "用户","交易类型", "消费金额单位元"))
    f  = open("gouwu_his.txt","r")
    for i in f:
        my_dic1 = json.loads(i)   #经过json.loads转换后，读取的字符串转换成了字典
        if user == my_dic1["name"]:  #根据用户名和传入的参数user比对，判断
            print ('%-22s%-22s%-11s%-14s%-9s' % (my_dic1["time"],ipaddr, my_dic1["name"],my_dic1["type"], my_dic1["money"]))


    #8调充值函数，转账函数
    chz_str=input("退出商城前，先给账户充点钱或者转个账，以备下次使用，输入c，充值;输入z,转账;输入c,z之外其他字符，不充值不转账，直接退出商城。请输入指令:")
    if chz_str == "c":
        chongzhi(user) #这里形参user，对应的实参是主函数的jack，tom（用户输入的）
    if chz_str == "z":
        zhuanzhang(user) #这里形参user，对应的实参是主函数的jack，tom（用户输入的）

#购物消费流水函数（记录每次结账花了多少钱，不单次记录买了多少商品，商品数量和价格在购物后打印出来）
def gouwu_his(user):
    pass
    #累加每次消费金额，求总的应还款
    ye_now= time.localtime()[0]  #当前日期的year取出来
    mon_now= time.localtime()[1]  #当前日期的mon取出来
    day_now= time.localtime()[2]  #当前日期的day取出来
    if mon_now-2<=0:
        yyyymmdd1 = "%s-%s-%s" % (2015,mon_now-2+12,22)
    else:
        yyyymmdd1 = "%s-%s-%s" % (2016,mon_now-2,22)
    yyyymmdd2 = "%s-%s-%s" % (2016,mon_now-1,22)
    yyyymmdd3 = "%s-%s-%s" % (2016,mon_now,10)
    zhangdan_start = time.mktime(time.strptime(yyyymmdd1,"%Y-%m-%d"))  #账单开始日期的时间戳
    zhangdan_end = time.mktime(time.strptime(yyyymmdd2,"%Y-%m-%d")) #账单结束日期的时间戳
    huankuanri = time.mktime(time.strptime(yyyymmdd3,"%Y-%m-%d"))  #还款日时间戳
    f  = open("gouwu_his.txt","r")
    my_li= [] #定义空列表
    for i in f: #遍历文件中的每行
        my_dic1 = json.loads(i) #没读取一行，将字符串转换成真正的字典
        time_stamp_now = time.mktime(time.strptime(my_dic1["time"],"%Y-%m-%d %H:%M:%S")) #购买结算时间折算成时间戳
        if time_stamp_now>zhangdan_start and time_stamp_now<zhangdan_end:
            my_li.append(my_dic1["money"]) #将遍历后的每次消费金额依次添加到列表
         #单独采用‘%s’时，直接输出字符串，
    # ‘%10s’表示在字符串前面添加占位符，并且字符串采用右对齐的方式，
    # ‘%-10s’表示在字符串后面添加占位符(这10位占位符包含字符串)，字符串采用左对齐的方式。
    #   例如字符串本身是"abc"3位，那么‘%-10s’表示在字符串"abc"后添加7位占位符

    print("============最近30天购物历史记录(信用卡对账单)============")
    print ("======================================================================================================")
    print ('%-10s%-15s%-15s%-26s%-13s%-15s' % ("用户名","账单编号", "账单日","账单日期范围", "还款日","应还款单位元"))
    d1 = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  #20160218171043
    d2 = datetime.date.today()  #2016-02-18
    d3 = yyyymmdd1  #2016-01-19至2016-02-18
    d4 = yyyymmdd3  #2016-02-28
    d5 = yyyymmdd2
    huankuanri = time.mktime(time.strptime(d4,"%Y-%m-%d"))#还款日对应的时间戳
    stamp2 = time.time()  #当前日期对应的时间戳
    n1 = divmod((stamp2-huankuanri),24*3600)[0] #逾期还款的天数

    # ye_now= time.localtime()[0]  #当前日期的year取出来
    # mon_now= time.localtime()[1]  #当前日期的month取出来
    # day_now= time.localtime()[2]  #当前日期的day取出来
    if day_now>=10 and day_now<=22:  #说明逾期，算息
        print ('%-10s%-20s%-20s%-7s至%-20s%-18s%-20s' % (my_dic1["name"],d1, d2,d3,d5,d4,sum(my_li)*1.0005**n1))
    else: #没有逾期，免息
        print ('%-10s%-20s%-20s%-7s至%-20s%-18s%-20s' % (my_dic1["name"],d1, d2,d3,d5,d4,sum(my_li)))
    print ("======================================================================================================")

    print ('%-20s%-20s%-9s%-9s%-9s' % ("时间","登录IP", "用户","交易类型", "消费金额单位元"))
    f  = open("gouwu_his.txt","r")
    for i in f:
        my_dic1 = json.loads(i)   #经过json.loads转换后，读取的字符串转换成了字典
        time_stamp_now = time.mktime(time.strptime(my_dic1["time"],"%Y-%m-%d %H:%M:%S")) #购买日期转换成时间戳
        #print(time.mktime(time.strptime("2016-02-01 20:30:48","%Y-%m-%d %H:%M:%S")))
        # 默认可以查询当前时间之前最近30天的购物消费流水 将字典中的格式化时间转换成时间戳和当前时间的前30天的时间戳比对（相对时间）
        if user == my_dic1["name"] and time_stamp_now>zhangdan_start and time_stamp_now<zhangdan_end:  #根据用户名和传入的参数user比对，判断
            print ('%-22s%-22s%-11s%-14s%-9s' % (my_dic1["time"],ipaddr, my_dic1["name"],my_dic1["type"], my_dic1["money"]))

#支付用户名密码验证
def login(username):   #这里的username是形参，实参是143行输入的意见注册的用户名，对应main函数的32行输入的用户名
    #1 json读出字典--文件中以字典的形式存储数据
    print("请验证支付用户名密码")
    q_data_login = select("username","bbb")
    # print(q_data_login)  #{'jack': {'times': 0, 'pwd': 123}, 'tom': {'times': 0, 'pwd': 123}}

    #2逻辑判断--字典中修改错误登录次数
    while True: #判断用户名，外循环，用于输入用户名
        # username = input("请输入用户名:")   验证支付密码的时候，不用再输入用户名了
        if len(username) == 0:  #判断用户名是否正确
            print("\033[31;1m用户名不能为空\033[0m")
        elif username not in q_data_login:
            print("\033[31;1m用户名不存在\033[0m")
        else:
            if q_data_login[username]["times"] >= 3 :  #判断错误登录次数是否大于等于3
                print("\033[31;1m账号锁定，请联系管理员\033[0m")
                break
            else:
                while True: #内循环，用于输入密码
                    passwd = int(input("请输入密码:"))  #这里输入的是字符串，文件中的密码是整数123的形式，所有转换成int，也可以把文件中的123变成"123"
                    if passwd == q_data_login[username]["pwd_zf"]:
                        q_data_login[username]["times"] =0
                        print("\033[32;1m登录成功\033[0m",username)
                        break_flag = True
                        # break  #跳出内循环
                        return  #这里返回的是None，计算器函数可以正常执行--162行
                    else: #密码不对，但是错误登录次数<3
                        q_data_login[username]["times"] += 1
                        times = q_data_login[username]["times"]
                        left_times = 3- times
                        if left_times ==0:
                            print("\033[31;1m账号锁定，请联系管理员\033[0m")
                            break_flag = True
                            break #跳出内循环
                            # return "\033[31;1m账号锁定，请联系管理员1\033[0m" #这里返回的不是None，162行函数return终止了，计算器函数就不执行了
                        else:
                            print("\033[31;1m密码输入错误，请重新输入，您还有 %s 次输入机会，3次密码输入错误，账号锁定" \
                                  "密码输入正确后，错误登录次数重置为0\033[0m" % (left_times))
                            continue #跳出内循环当次迭代
                if break_flag:  #跳出外循环，和39行while同一级
                    break  #跳出外循环

    #3将修改后的错误登录次数写入文件
    f = open("username1.txt","w") #新建一个新文件
    json.dump(q_data_login,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_mima转换后写入f）
    f.close()

#二atm函数
#充值函数，余额不够了，给余额充钱，手动输入充值金额,将充值金额写入余额表
# 5、连续多次充值，只记录了最后一次充值记录--ok
#    用户的余额是对的，已经写入文件了，就是充值记录值记录了最后一次--ok
#    原因分析：因为分成了2个函数，1个充值函数专门用来处理余额的变动，另外1个充值函数专门处理新增加充值记录，打印充值记录
#    充值记录函数需要调用充值函数，显示充值金额，但是充值函数只有在退出的时候return，无法在多次充值的时候return充值金额
#    解决办法：将充值记录函数合并到充值函数，就可以直接调用充值金额，不需要充值函数return了
def chongzhi(user):  #这里形参user，对应的实参是主函数的jack，tom（用户输入的）
    #1充值后变动余额表
    ipaddr = socket.gethostbyname(socket.gethostname())  #记录登录ip
    break_flag =False
    while True:
        try:
            chz_input = int(input("请输入需要充值的金额:"))  #字符串转换成int用于余额的计算
        except:
            chz_input = int(input("\033[31;1m充值金额必须是数字，请重新输入\033[0m:"))
        q_data_yue = select("yue","ddd")
        q_data_yue[user]["yue"] += chz_input #更改余额字段(在原来余额的基础上新增加输入的余额)

        f = open("username1.txt","w") #新建一个新文件
        # f.seek(0)
        json.dump(q_data_yue,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_yue转换后写入f）
        f.close()
        print("\033[32;1m充值成功,充值金额[%s]元,[%s]当前余额是[%s]元\033[0m" % (chz_input,user,q_data_yue[user]["yue"]))

        #2充值后，新建一个充值记录表
        #构造字典，往字典添加键值对，写入到文件
        # dic ={"k1":"v1","k2":"v2"}
        # my_dic1[time.time()] = {'name':user, 'money': chongzhi(user),"type":"chongzhi","time":time.strftime('%Y-%m-%d %H:%M:%S')}
        my_dic1 = {'name':user,"ipaddr":ipaddr, 'money': chz_input,"type":"chongzhi","time":time.strftime('%Y-%m-%d %H:%M:%S')}
        # print(my_dic1)

        j_str = json.dumps(my_dic1)  #先把字典转换成字符串
        f = open("chongzhi.txt","a")  #a模式、追加内容到文件最后
        f.write(j_str)   #再写入到文件
        f.write("\n")   #添加换行符  这里手动添加换行
        # f.write(data) #直接写入字典，报错 TypeError: write() argument must be str, not dict
        f.close()

        # f = open("chongzhi.txt","a") #新建一个新文件
        # # f.seek(0)
        # json.dump(my_dic1,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_yue转换后写入f）
        # f.close()

        #3将充值记录表的内容打印出来--日志（时间，地点，人物，事件）
    #将历史充值记录打印出来  问题1：多个字典在同一行  解决办法：通过317行dumps后，手动write换行符"\n"
    #问题2：由于字典是独立的，一次json读取多个字典会报错340行，改为像处理文件一样一行行读取，读一行把内容json.loads一下，就是字典
        print("---ATM充值历史记录---")
        print ('%-20s%-20s%-9s%-9s%-9s' % ("时间","登录IP", "用户","交易类型", "交易金额单位元"))
        f  = open("chongzhi.txt","r")
        for i in f:
            my_dic1 = json.loads(i)   #经过json.loads转换后，读取的字符串转换成了字典
            # print(my_dic1)  #{"k1": "v1", "k2": "v2"}
        # print(type(my_dic1)) #<class 'dict'>
        # q_data_jilu = select("jilu","bbb")
        # print(q_data_jilu)
            if user == my_dic1["name"]:  #根据用户名和传入的参数user比对，判断
                print ('%-22s%-22s%-11s%-14s%-9s' % (my_dic1["time"],ipaddr, my_dic1["name"],my_dic1["type"], my_dic1["money"]))

        while True:
            tuichu_cz = input("确认退出充值程序么？输入c，退出充值回到主菜单；输入a，继续充值:")
            if tuichu_cz == "a":
                # return chz_input
                break  #跳出循环的当前迭代，回到75行
            elif tuichu_cz == "c":
                break_flag = True  #外循环跳出标签
                break
            else:  #如果输入的不是a或者c
                print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
                continue  #跳出内循环本次迭代
                # print total
        if break_flag:
            # return chz_input
            break  #跳出外循环

#转账函数
def zhuanzhang(user):
    ipaddr = socket.gethostbyname(socket.gethostname())  #记录登录ip
    #转出方
    break_flag =False
    while True:
        try:
            zhc_input = int(input("请输入需要转出的金额:"))  #字符串转换成int用于余额的计算
        except:
            zhc_input = int(input("\033[31;1m转出金额必须是数字，请重新输入\033[0m:"))
        while True:
            to_input = input("请输入收款人:")  #字符串转换成int用于余额的计算
            q_data_yue = select("yue","ddd")
            if to_input in q_data_yue:
                q_data_yue[user]["yue"] -= zhc_input #更改余额字段(在原来余额的基础上新增加输入的余额)
                # print(q_data_yue[user]["yue"])

                f = open("username1.txt","w") #新建一个新文件
                # f.seek(0)
                json.dump(q_data_yue,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_yue转换后写入f）
                f.close()
                break
            else:
                print("\033[31;1m收款人不存在，请重新输入收款人\033[0m")

        #收款人
        q_data_yue = select("yue","ddd")
        q_data_yue[to_input]["yue"] += zhc_input #更改余额字段(在原来余额的基础上新增加转出方转出的余额)
        # print(q_data_yue[to_input]["yue"])

        f = open("username1.txt","w") #新建一个新文件
        # f.seek(0)
        json.dump(q_data_yue,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_yue转换后写入f）
        f.close()
        print("\033[32;1m转账成功,转出方[%s]当前余额[%s]元,收款人[%s]当前余额[%s]元,转账金额[%s]元,\033[0m" % (user,q_data_yue[user]["yue"],to_input,q_data_yue[to_input]["yue"],zhc_input))

        #2转账后，新建一个转账记录表
        #构造字典，往字典添加键值对，写入到文件
        # dic ={"k1":"v1","k2":"v2"}
        # my_dic1[time.time()] = {'name':user, 'money': chongzhi(user),"type":"chongzhi","time":time.strftime('%Y-%m-%d %H:%M:%S')}
        my_dic1 = {'name':user,'to':to_input,"ipaddr":ipaddr, 'money': zhc_input,"type":"zhuanzhang_out","time":time.strftime('%Y-%m-%d %H:%M:%S')}
        my_dic2 = {'name':to_input,'from':user,"ipaddr":ipaddr, 'money': zhc_input,"type":"zhuanzhang_in","time":time.strftime('%Y-%m-%d %H:%M:%S')}
        # print(my_dic1)
        # print(my_dic1["to"])

        j_str = json.dumps(my_dic1)  #先把字典转换成字符串
        j_str2 = json.dumps(my_dic2)
        f = open("chongzhi.txt","a")
        f.write(j_str)   #再写入到文件
        f.write("\n")
        f.write(j_str2)
        f.write("\n")   #添加换行符  这里手动添加换行
        # f.write(data) #直接写入字典，报错 TypeError: write() argument must be str, not dict
        f.close()

        # f = open("chongzhi.txt","a") #新建一个新文件
        # # f.seek(0)
        # json.dump(my_dic1,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_yue转换后写入f）
        # f.close()

        #3将充值记录表的内容打印出来--日志（时间，地点，人物，事件）
    #将历史充值记录打印出来  问题1：多个字典在同一行  解决办法：通过317行dumps后，手动write换行符"\n"
    #问题2：由于字典是独立的，一次json读取多个字典会报错340行，改为像处理文件一样一行行读取，读一行把内容json.loads一下，就是字典
        print("---ATM转账历史记录---")
        print ('%-20s%-20s%-9s%-9s%-9s%-9s' % ("时间","登录IP", "用户","交易类型", "交易金额单位元","收款人"))
        f  = open("chongzhi.txt","r")
        for i in f:
            my_dic1 = json.loads(i)   #经过json.loads转换后，读取的字符串转换成了字典
            # print(my_dic1)  #{"k1": "v1", "k2": "v2"}
        # print(type(my_dic1)) #<class 'dict'>
        # q_data_jilu = select("jilu","bbb")
        # print(q_data_jilu)
            if user == my_dic1["name"]:  #根据用户名和传入的参数user比对，判断
                print ('%-22s%-22s%-11s%-14s%-16s%-9s' % (my_dic1["time"],ipaddr, my_dic1["name"],my_dic1["type"], my_dic1["money"],my_dic1["to"]))


        while True:
            tuichu_zz = input("确认退出转账程序么？输入c，退出转账回到主菜单；输入a，继续转账:")
            if tuichu_zz == "a":
                break  #跳出循环的当前迭代，回到75行
            elif tuichu_zz == "c":
                break_flag = True  #外循环跳出标签
                break
            else:  #如果输入的不是a或者c
                print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
                continue  #跳出内循环本次迭代
        if break_flag:
            break  #跳出外循环

#查询余额接口
def chaxunyue(user):
    ipaddr = socket.gethostbyname(socket.gethostname())  #记录登录ip
    break_flag =False
    while True:
        q_data_yue = select("yue","ddd")
        print("\033[32;1m当前用户的余额是：\033[0m",q_data_yue[user]["yue"])

        #2查询余额后，新建一个查询余额记录表
        #构造字典，往字典添加键值对，写入到文件
        my_dic1 = {'name':user,"ipaddr":ipaddr, 'money': "N/A","type":"chaxunyue","time":time.strftime('%Y-%m-%d %H:%M:%S')}
        # print(my_dic1)

        j_str = json.dumps(my_dic1)  #先把字典转换成字符串
        f = open("chongzhi.txt","a")
        f.write(j_str)   #再写入到文件
        f.write("\n")   #添加换行符  这里手动添加换行
        # f.write(data) #直接写入字典，报错 TypeError: write() argument must be str, not dict
        f.close()

        #3将查询记录表的内容打印出来--日志（时间，地点，人物，事件）
    #将历史充值记录打印出来  问题1：多个字典在同一行  解决办法：通过317行dumps后，手动write换行符"\n"
    #问题2：由于字典是独立的，一次json读取多个字典会报错340行，改为像处理文件一样一行行读取，读一行把内容json.loads一下，就是字典
        print("---ATM查询余额历史记录---")
        print ('%-20s%-20s%-9s%-9s%-9s' % ("时间","登录IP", "用户","交易类型", "交易金额单位元"))
        f  = open("chongzhi.txt","r")
        for i in f:
            my_dic1 = json.loads(i)   #经过json.loads转换后，读取的字符串转换成了字典
            if user == my_dic1["name"]:  #根据用户名和传入的参数user比对，判断
                print ('%-22s%-22s%-11s%-14s%-9s' % (my_dic1["time"],ipaddr, my_dic1["name"],my_dic1["type"], my_dic1["money"]))

        while True:
            tuichu_cx = input("确认退出查询余额么？输入c，退出查询余额回到主菜单；输入a，继续查询余额:")
            if tuichu_cx == "a":
                break  #跳出循环的当前迭代，回到75行
            elif tuichu_cx == "c":
                break_flag = True  #外循环跳出标签
                break
            else:  #如果输入的不是a或者c
                print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
                continue  #跳出内循环本次迭代
        if break_flag:
            break  #跳出外循环

#atm取款接口(支付接口--连接商城)
def qukuan(user):
    break_flag =False
    while True:
        #1变动余额表
        # quk_input = int(input("请输入需要取出的金额:"))
        try:
            quk_input = int(input("请输入需要取出的金额:"))  #字符串转换成int用于余额的计算
        except:
            quk_input = int(input("\033[31;1m取出金额必须是数字，请重新输入\033[0m:"))
        q_data_yue = select("yue","ddd")
        q_data_yue[user]["yue"] -= quk_input #更改余额字段(在原来余额的基础上减去输入的余额)
        # print(q_data_yue[user]["yue"])

        f = open("username1.txt","w") #新建一个新文件
        # f.seek(0)
        json.dump(q_data_yue,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_yue转换后写入f）
        f.close()
        print("\033[32;1m取款成功,取款人[%s],当前余额[%s]元,取款金额[%s]元,\033[0m"% (user,q_data_yue[user]["yue"],quk_input))

        #2取款后，新建一个取款历史记录表
        #构造字典，往字典添加键值对，写入到文件
        my_dic1 = {'name':user,"ipaddr":ipaddr, 'money': quk_input,"type":"qukuan","time":time.strftime('%Y-%m-%d %H:%M:%S')}
        # print(my_dic1)

        j_str = json.dumps(my_dic1)  #先把字典转换成字符串
        f = open("chongzhi.txt","a")  #往原有的文件中追加取款记录
        f.write(j_str)   #再写入到文件
        f.write("\n")   #添加换行符  这里手动添加换行
        # f.write(data) #直接写入字典，报错 TypeError: write() argument must be str, not dict
        f.close()

        #3将取款记录表的内容打印出来--日志（时间，地点，人物，事件）
    #将历史记录打印出来  问题1：多个字典在同一行  解决办法：通过317行dumps后，手动write换行符"\n"
    #问题2：由于字典是独立的，一次json读取多个字典会报错340行，改为像处理文件一样一行行读取，读一行把内容json.loads一下，就是字典
        print("---ATM取款历史记录---")
        print ('%-20s%-20s%-9s%-9s%-9s' % ("时间","登录IP", "用户","交易类型", "交易金额单位元"))
        f  = open("chongzhi.txt","r")
        for i in f:
            my_dic1 = json.loads(i)   #经过json.loads转换后，读取的字符串转换成了字典
            if user == my_dic1["name"]:  #根据用户名和传入的参数user比对，判断
                print ('%-22s%-22s%-11s%-14s%-9s' % (my_dic1["time"],ipaddr, my_dic1["name"],my_dic1["type"], my_dic1["money"]))

        while True:
            tuichu_qk = input("确认退出取款程序么？输入c，退出取款回到主菜单；输入a，继续取款:")
            if tuichu_qk == "a":
                break  #跳出循环的当前迭代，回到75行
            elif tuichu_qk == "c":
                break_flag = True  #外循环跳出标签
                break
            else:  #如果输入的不是a或者c
                print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
                continue  #跳出内循环本次迭代
        if break_flag:
            break  #跳出外循环

#提现函数（模拟信用卡提现，手续费5%）
def tixian(user):
    pass
    break_flag =False
    while True:
        #1变动余额表
        try:
            tix_input = int(input("请输入需要提现的金额:"))  #字符串转换成int用于余额的计算
        except:
            tix_input = int(input("\033[31;1m提现金额必须是数字，请重新输入\033[0m:"))
        q_data_yue = select("yue","ddd")
        q_data_yue[user]["yue"] -= tix_input*1.05 #更改余额字段(在原来余额的基础上减去输入的余额和手续费)
        # print(q_data_yue[user]["yue"])   这里5%的手续费

        f = open("username1.txt","w") #新建一个新文件
        # f.seek(0)
        json.dump(q_data_yue,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_yue转换后写入f）
        f.close()
        print("\033[32;1m提现成功,提现人[%s],当前余额[%s]元,提现金额[%s]元,提现手续费[%s]元\033[0m"% (user,q_data_yue[user]["yue"],tix_input,tix_input*0.05))

        #2提现后，新建一个历史记录表
        #构造字典，往字典添加键值对，写入到文件
        my_dic1 = {'name':user,"ipaddr":ipaddr, 'money': tix_input,'shouxufei': tix_input*0.05,"type":"tixian","time":time.strftime('%Y-%m-%d %H:%M:%S')}
        # print(my_dic1)

        j_str = json.dumps(my_dic1)  #先把字典转换成字符串
        f = open("chongzhi.txt","a")  #往原有的文件中追加提现记录
        f.write(j_str)   #再写入到文件
        f.write("\n")   #添加换行符  这里手动添加换行
        # f.write(data) #直接写入字典，报错 TypeError: write() argument must be str, not dict
        f.close()

        #3将提现记录表的内容打印出来--日志（时间，地点，人物，事件）
    #将历史记录打印出来  问题1：多个字典在同一行  解决办法：通过317行dumps后，手动write换行符"\n"
    #问题2：由于字典是独立的，一次json读取多个字典会报错340行，改为像处理文件一样一行行读取，读一行把内容json.loads一下，就是字典
        print("---ATM信用卡提现历史记录---")
        print ('%-20s%-20s%-9s%-9s%-9s%-9s' % ("时间","登录IP", "用户","交易类型", "交易金额单位元","手续费"))
        f  = open("chongzhi.txt","r")
        for i in f:
            my_dic1 = json.loads(i)   #经过json.loads转换后，读取的字符串转换成了字典
            if user == my_dic1["name"]:  #根据用户名和传入的参数user比对，判断
                print ('%-22s%-22s%-11s%-14s%-15s%-9s' % (my_dic1["time"],ipaddr, my_dic1["name"],my_dic1["type"], my_dic1["money"],my_dic1["shouxufei"]))

        while True:
            tuichu_tx = input("确认退出提现程序么？输入c，退出提现回到主菜单；输入a，继续提现:")
            if tuichu_tx == "a":
                break  #跳出循环的当前迭代，回到75行
            elif tuichu_tx == "c":
                break_flag = True  #外循环跳出标签
                break
            else:  #如果输入的不是a或者c
                print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
                continue  #跳出内循环本次迭代
        if break_flag:
            break  #跳出外循环

#预算调整
def yusuan(user):
    break_flag =False
    while True:
        # yusuan_input = int(input("请输入需要调整的预算额度，输入正数，表示增加预算额度；输入负数，表示减少预算额度:"))  #字符串转换成int用于余额的计算
        try:
            yusuan_input = int(input("请输入需要调整的预算额度，输入正数，表示增加预算额度；输入负数，表示减少预算额度:"))  #字符串转换成int用于余额的计算
        except:
            yusuan_input = int(input("\033[31;1m预算调整额度必须是数字，请重新输入\033[0m:"))
        q_data_yusuan = select("yue","bbb")
        q_data_yusuan[user]["yusuan"] += yusuan_input #更改预算字段(在原来预算的基础上新增加或者减少输入的额度)

        f = open("username1.txt","w") #新建一个新文件
        # f.seek(0)
        json.dump(q_data_yusuan,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_yue转换后写入f）
        f.close()
        print("\033[32;1m预算调整成功,预算调整额度[%s]元,[%s]当前预算是[%s]元\033[0m" % (yusuan_input,user,q_data_yusuan[user]["yusuan"]))

        #2预算调整后，新建一个预算调整历史记录表
        #构造字典，往字典添加键值对，写入到文件
        my_dic1 = {'name':user,"ipaddr":ipaddr, 'money': yusuan_input,"type":"yusuantz","time":time.strftime('%Y-%m-%d %H:%M:%S')}
        # print(my_dic1)

        j_str = json.dumps(my_dic1)  #先把字典转换成字符串
        f = open("chongzhi.txt","a")  #往原有的文件中追加取款记录
        f.write(j_str)   #再写入到文件
        f.write("\n")   #添加换行符  这里手动添加换行
        # f.write(data) #直接写入字典，报错 TypeError: write() argument must be str, not dict
        f.close()

        #3将预算调整记录表的内容打印出来--日志（时间，地点，人物，事件）
    #将历史记录打印出来  问题1：多个字典在同一行  解决办法：通过317行dumps后，手动write换行符"\n"
    #问题2：由于字典是独立的，一次json读取多个字典会报错340行，改为像处理文件一样一行行读取，读一行把内容json.loads一下，就是字典
        print("---ATM预算调整历史记录---")
        print ('%-20s%-20s%-9s%-9s%-9s' % ("时间","登录IP", "用户","交易类型", "交易金额单位元"))
        f  = open("chongzhi.txt","r")
        for i in f:
            my_dic1 = json.loads(i)   #经过json.loads转换后，读取的字符串转换成了字典
            if user == my_dic1["name"]:  #根据用户名和传入的参数user比对，判断
                print ('%-22s%-22s%-11s%-14s%-9s' % (my_dic1["time"],ipaddr, my_dic1["name"],my_dic1["type"], my_dic1["money"]))

        while True:
            tuichu_ys = input("确认退出预算调整程序么？输入c，退出回到主菜单；输入a，继续:")
            if tuichu_ys == "a":
                break  #跳出循环的当前迭代，回到75行
            elif tuichu_ys == "c":
                break_flag = True  #外循环跳出标签
                break
            else:  #如果输入的不是a或者c
                print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
                continue  #跳出内循环本次迭代
        if break_flag:
            break  #跳出外循环

#修改登录密码--ok
def xiugaimima(user):
    break_flag =False
    while True:
        mima_input_old = int(input("密码修改前，请先输入旧密码:"))
        q_data_mima = select("username","bbb")
        if q_data_mima[user]["pwd"] == mima_input_old:
            mima_input = int(input("请输入新密码:"))  #字符串转换成int用于余额的计算(修改密码的话，不涉及计算，可以不用转换成int)
        # q_data_mima = select("username","bbb")
            q_data_mima[user]["pwd"] = mima_input #更改密码字段

            f = open("username1.txt","w") #新建一个新文件
            # f.seek(0)
            json.dump(q_data_mima,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_mima转换后写入f）
            f.close()
            print("\033[32;1m密码修改成功,新密码是[%s]\033[0m" % (q_data_mima[user]["pwd"]))

            #2修改登录密码后，新建一个历史记录表
            #构造字典，往字典添加键值对，写入到文件
            my_dic1 = {'name':user,"ipaddr":ipaddr, 'money': "N/A","type":"mimaxg_dl","time":time.strftime('%Y-%m-%d %H:%M:%S')}
            # print(my_dic1)

            j_str = json.dumps(my_dic1)  #先把字典转换成字符串
            f = open("chongzhi.txt","a")  #往原有的文件中追加取款记录
            f.write(j_str)   #再写入到文件
            f.write("\n")   #添加换行符  这里手动添加换行
            # f.write(data) #直接写入字典，报错 TypeError: write() argument must be str, not dict
            f.close()

            #3将修改登录密码记录表的内容打印出来--日志（时间，地点，人物，事件）
        #将历史记录打印出来  问题1：多个字典在同一行  解决办法：通过317行dumps后，手动write换行符"\n"
        #问题2：由于字典是独立的，一次json读取多个字典会报错340行，改为像处理文件一样一行行读取，读一行把内容json.loads一下，就是字典
            print("---ATM修改登录密码历史记录---")
            print ('%-20s%-20s%-9s%-9s%-9s' % ("时间","登录IP", "用户","交易类型", "交易金额单位元"))
            f  = open("chongzhi.txt","r")
            for i in f:
                my_dic1 = json.loads(i)   #经过json.loads转换后，读取的字符串转换成了字典
                if user == my_dic1["name"]:  #根据用户名和传入的参数user比对，判断
                    print ('%-22s%-22s%-11s%-14s%-9s' % (my_dic1["time"],ipaddr, my_dic1["name"],my_dic1["type"], my_dic1["money"]))

            while True:
                tuichu_mmxg = input("确认退出密码修改程序么？输入c，退出回到主菜单；输入a，继续:")
                if tuichu_mmxg == "a":
                    # return chz_input
                    break  #跳出循环的当前迭代，回到75行
                elif tuichu_mmxg == "c":
                    break_flag = True  #外循环跳出标签
                    break
                else:  #如果输入的不是a或者c
                    print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
                    continue  #跳出内循环本次迭代
                    # print total
            if break_flag:
                return mima_input
                break  #跳出外循环
        else:
            print("\033[31;1m旧密码验证错误\033[0m")

#修改支付密码--nok
def xiugaimima_zf(user):
    break_flag =False
    while True:
        mima_input_old = int(input("支付密码修改前，请先输入旧密码:"))
        q_data_mima_zf = select("username","bbb")
        if q_data_mima_zf[user]["pwd_zf"] == mima_input_old:
            mima_input = int(input("请输入新密码:"))  #字符串转换成int用于余额的计算(修改密码的话，不涉及计算，可以不用转换成int)
        # q_data_mima = select("username","bbb")
            q_data_mima_zf[user]["pwd_zf"] = mima_input #更改密码字段

            f = open("username1.txt","w") #新建一个新文件
            # f.seek(0)
            json.dump(q_data_mima_zf,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_mima转换后写入f）
            f.close()
            print("\033[32;1m支付密码修改成功,新密码是[%s]\033[0m" % (q_data_mima_zf[user]["pwd_zf"]))

            #2修改支付密码后，新建一个历史记录表
            #构造字典，往字典添加键值对，写入到文件
            my_dic1 = {'name':user,"ipaddr":ipaddr, 'money': "N/A","type":"mimaxg_zf","time":time.strftime('%Y-%m-%d %H:%M:%S')}
            # print(my_dic1)

            j_str = json.dumps(my_dic1)  #先把字典转换成字符串
            f = open("chongzhi.txt","a")  #往原有的文件中追加取款记录
            f.write(j_str)   #再写入到文件
            f.write("\n")   #添加换行符  这里手动添加换行
            # f.write(data) #直接写入字典，报错 TypeError: write() argument must be str, not dict
            f.close()

            #3将修改支付密码记录表的内容打印出来--日志（时间，地点，人物，事件）
        #将历史记录打印出来  问题1：多个字典在同一行  解决办法：通过317行dumps后，手动write换行符"\n"
        #问题2：由于字典是独立的，一次json读取多个字典会报错340行，改为像处理文件一样一行行读取，读一行把内容json.loads一下，就是字典
            print("---ATM修改支付密码历史记录---")
            print ('%-20s%-20s%-9s%-9s%-9s' % ("时间","登录IP", "用户","交易类型", "交易金额单位元"))
            f  = open("chongzhi.txt","r")
            for i in f:
                my_dic1 = json.loads(i)   #经过json.loads转换后，读取的字符串转换成了字典
                if user == my_dic1["name"]:  #根据用户名和传入的参数user比对，判断
                    print ('%-22s%-22s%-11s%-14s%-9s' % (my_dic1["time"],ipaddr, my_dic1["name"],my_dic1["type"], my_dic1["money"]))

            while True:
                tuichu_mmxg = input("确认退出支付密码修改程序么？输入c，退出回到主菜单；输入a，继续:")
                if tuichu_mmxg == "a":
                    # return chz_input
                    break  #跳出循环的当前迭代，回到75行
                elif tuichu_mmxg == "c":
                    break_flag = True  #外循环跳出标签
                    break
                else:  #如果输入的不是a或者c
                    print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
                    continue  #跳出内循环本次迭代
                    # print total
            if break_flag:
                return mima_input
                break  #跳出外循环
        else:
            print("\033[31;1m旧支付密码验证错误\033[0m")

#查询ATM操作历史记录
def history_ATM(user):
    pass
    print("==========ATM操作历史记录==========")
    print ('%-20s%-20s%-9s%-9s%-9s' % ("时间","登录IP", "用户","交易类型", "交易金额单位元"))
    f  = open("chongzhi.txt","r")
    for i in f:
        my_dic1 = json.loads(i)   #经过json.loads转换后，读取的字符串转换成了字典
        if user == my_dic1["name"]:  #根据用户名和传入的参数user比对，判断
            print ('%-22s%-22s%-11s%-14s%-9s' % (my_dic1["time"],ipaddr, my_dic1["name"],my_dic1["type"], my_dic1["money"]))

#三、管理接口
#添加用户（注册用户）
def adduser():
    #1变动用户表
    break_flag =False
    while True:
        user_input = input("请输入需要添加的用户名:")
        # 1读出用户表到字典
        q_data_user = select("username","bbb")
        #2添加键值对到字典（用户名自定义输入，初始登录密码，初始余额，初始预算，初始错误登录次数,初始冻结状态，初始支付密码都给默认值）
        q_data_user[user_input] = {"pwd": 123, "times": 0,"yue": 200000, "yusuan": 200000,"status":"active","pwd_zf": 124}
        #3将添加键值对后的字典，重新写入到文件json
        f = open("username1.txt","w") #新建一个新文件
        # f.seek(0)
        json.dump(q_data_user,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_user转换后写入f）
        f.close()
        print("\033[32;1m用户添加成功,新用户是[%s]，初始密码是[%s]，初始余额是[%s]元，初始预算是[%s]元,初始可用状态是[%s],初始支付密码是[%s]\033[0m" % (user_input,q_data_user[user_input]["pwd"],q_data_user[user_input]["yue"],q_data_user[user_input]["yusuan"],q_data_user[user_input]["status"],q_data_user[user_input]["pwd_zf"]))

        #2变动商品表(添加用户表的同时，商品表也同步增加这个用户)
        q_data_shop = select("shop","bbb")
        #2添加键值对到字典（用户名自定义输入，初始密码，初始余额，初始预算，初始错误登录次数都给默认值）
        q_data_shop[user_input] = {"2": {"price": 8000, "goods": "mac", "times": 0}, "1": {"price": 6000, "goods": "iphone6s", "times": 0}}
        #3将添加键值对后的字典，重新写入到文件json
        f = open("shop.txt","w") #新建一个新文件
        # f.seek(0)
        json.dump(q_data_shop,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_user转换后写入f）
        f.close()

        while True:
            tuichu_adduser = input("确认退出添加用户程序么？输入c，退出回到主菜单；输入a，继续:")
            if tuichu_adduser == "a":
                break  #跳出循环的当前迭代
            elif tuichu_adduser == "c":
                break_flag = True  #外循环跳出标签
                break
            else:  #如果输入的不是a或者c
                print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
                continue  #跳出内循环本次迭代
        if break_flag:
            # return tuichu_adduser
            break  #跳出外循环

#删除用户（注销用户）
def deluser():
    #1变动用户表
    break_flag =False
    while True:
        user_input = input("请输入需要删除的用户名:")
        # 1读出用户表到字典
        q_data_user = select("username","bbb")
        # q_data_shop = select("shop","bbb")
        #2删除键值对从字典
        if user_input in q_data_user:
            q_data_user.pop(user_input) #user_input不能加引号
            #3将添加键值对后的字典，重新写入到文件json
            f = open("username1.txt","w") #新建一个新文件
            # f.seek(0)
            json.dump(q_data_user,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_user转换后写入f）
            f.close()
            print("\033[32;1m用户删除成功,被删除的用户是[%s]\033[0m" % user_input)

        #2变动商品表(删除用户表用户的同时，商品表也同步删除这个用户，否则商品表会多一些历史数据，即已经销户的用户的购买记录，已经销户的用户的购买记录可以单独存在历史表中，用于对账)
        q_data_shop = select("shop","bbb")
        #2删除键值对从字典
        if user_input in q_data_shop:
            q_data_shop.pop(user_input) #user_input不能加引号
            #3将添加键值对后的字典，重新写入到文件json
            f = open("shop.txt","w") #新建一个新文件
            # f.seek(0)
            json.dump(q_data_shop,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_user转换后写入f）
            f.close()

            while True:
                tuichu_deluser = input("确认退出删除用户程序么？输入c，退出；输入a，继续:")
                if tuichu_deluser == "a":
                    break  #跳出循环的当前迭代
                elif tuichu_deluser == "c":
                    break_flag = True  #外循环跳出标签
                    break
                else:  #如果输入的不是a或者c
                    print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
                    continue  #跳出内循环本次迭代
            if break_flag:
                # return tuichu_deluser
                break  #跳出外循
        else:
            print("\033[31;1m您要删除的用户不存在\033[0m")

#查询用户信息
def viewuser():
    break_flag = False
    while True:
        user_input = input("请输入需要查询的用户名:")
            # 1读出用户表到字典
        q_data_user = select("username","bbb")
        if user_input in q_data_user:
            print("---用户信息---")
            print ('%-8s%-9s%-9s%-9s' % ("用户名", "密码","余额(单位元)", "预算(单位元)"))
            print ('%-11s%-11s%-14s%-11s' % (user_input, q_data_user[user_input]["pwd"],q_data_user[user_input]["yue"], q_data_user[user_input]["yusuan"]))

            while True:
                tuichu_viewuser = input("确认退出查询用户程序么？输入c，回到主菜单；输入a，继续:")
                if tuichu_viewuser == "a":
                    break  #跳出循环的当前迭代
                elif tuichu_viewuser == "c":
                    break_flag = True  #外循环跳出标签
                    break
                else:  #如果输入的不是a或者c
                    print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
                    continue  #跳出内循环本次迭代
            if break_flag:
                # return tuichu_adduser
                break  #跳出外循环
        else:
            print("\033[31;1m您要查询的用户不存在\033[0m")

#冻结用户
def inactiveuser():
    pass
    break_flag =False
    while True:
        user_input = input("请输入需要冻结的用户名:")
        # 1读出用户表到字典
        q_data_user = select("username","bbb")
        # 2修改字典的status的状态
        if user_input in q_data_user: #and q_data_user[user_input]["status"] != "inactive":
            q_data_user[user_input]["status"]= "inactive"
        # 3将修改后的字典，重新写入到文件json
            f = open("username1.txt","w") #新建一个新文件
            # f.seek(0)
            json.dump(q_data_user,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_user转换后写入f）
            f.close()
            print("\033[31;1m用户[%s]被冻结，请联系管理员\033[0m" % user_input)
            while True:
                tuichu_inactiveuser = input("确认退出冻结用户程序么？输入c，回到主菜单；输入a，继续:")
                if tuichu_inactiveuser == "a":
                    break  #跳出循环的当前迭代
                elif tuichu_inactiveuser == "c":
                    break_flag = True  #外循环跳出标签
                    break
                else:  #如果输入的不是a或者c
                    print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
                    continue  #跳出内循环本次迭代
            if break_flag:
                # return tuichu_adduser
                break  #跳出外循环
        # elif user_input in q_data_user and q_data_user[user_input]["status"] == "inactive":
        #     print("\033[31;1m用户[%s]的当前状态已经是冻结不可用状态\033[0m" % user_input)
        else:
            print("\033[31;1m您要冻结的用户不存在\033[0m")

#解冻用户
def activeuser():
    pass
    break_flag =False
    while True:
        user_input = input("请输入需要解冻的用户名:")
        # 1读出用户表到字典
        q_data_user = select("username","bbb")
        # 2修改字典的status的状态
        if user_input in q_data_user:
            q_data_user[user_input]["status"]= "active"
        # 3将修改后的字典，重新写入到文件json
            f = open("username1.txt","w") #新建一个新文件
            # f.seek(0)
            json.dump(q_data_user,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_user转换后写入f）
            f.close()
            print("\033[32;1m用户[%s]被解冻\033[0m" % user_input)
            while True:
                tuichu_inactiveuser = input("确认退出解冻用户程序么？输入c，回到主菜单；输入a，继续:")
                if tuichu_inactiveuser == "a":
                    break  #跳出循环的当前迭代
                elif tuichu_inactiveuser == "c":
                    break_flag = True  #外循环跳出标签
                    break
                else:  #如果输入的不是a或者c
                    print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
                    continue  #跳出内循环本次迭代
            if break_flag:
                # return tuichu_adduser
                break  #跳出外循环
        else:
            print("\033[31;1m您要解冻的用户不存在\033[0m")











