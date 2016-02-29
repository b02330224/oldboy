__author__ = 'Administrator'
#-*- coding:utf-8 -*-
import json
import time
import datetime
import socket
import sys
import random
import logging
# print(sys.path) #默认路径是当前py文件的父目录

#踩过的坑：
#1、如果是life_value-=10就会出现生命值不变的情况，需要用q_data_life[user]["life_value"] -=10才行

from backend.db.sql_api import select
# from backend.db import json2
#from 模块 import 方法名字（函数名字）

ipaddr = socket.gethostbyname(socket.gethostname())  #记录登录ip，定义成全局变量

class Role(object): #定义新式类 定义一个类， class是定义类的语法，Role是类名，(object)是新式类的写法
    def __init__(self,name,role,weapon,life_value =100,money=15000): #初始化方法（构造方法），实例化的时候默认调用        #初始化方法，在生成一个角色时要初始化的一些属性就填写在这里
        """
        :param name: 用户名
        :param role:角色名
        :param weapon:武器
        :param life_value:生命值
        :param money:金币
        :return:
        """
        self.name = name  #把24行实例r1的实际参数"jack"通过形参name传递给r1.name
        self.role = role  #角色名
        self.weapon = weapon #武器
        self.life_value = life_value #生命值
        self.money = money #金币

#1标准日志方法，可以往文件记录日志，也可以打印出来
    def log1(self):
        pass #logging的日志可以从低到高依次分为 debug(), info(), warning(), error() and critical() 5个级别
        logger = logging.getLogger("TEST_LOG") #创建日志对象
        logger.setLevel(logging.CRITICAL)  #定义全局日志级别（DEBUG必须大写）

        sh = logging.StreamHandler()  #创建屏幕句柄--全局日志级别和屏幕日志级别，按级别高的来
        sh.setLevel(logging.DEBUG)  #定义屏幕打印日志级别（DEBUG必须大写）

        fh = logging.FileHandler("access.log") #创建文件句柄--全局日志级别和文件日志级别，按级别高的来
        fh.setLevel(logging.WARNING)  #定义文件中日志级别（WARNING必须大写）

        formatter= logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(message)s-%(filename)s") #定义日志格式
        #%(name)s  指的是  TEST-LOG
        # %(asctime)s指的是日志时间 2016-02-22 22:55:24 到毫秒
        # %(levelname)s 指的是日志级别 WARNING
        # %(message)s 指的是日志信息 warn message
        # %(filename)s可以区别是哪个模块输出的日志  03 writefileview.py（带py）
        # %(created)s 指的时间戳1456153718.13236
        # %(levelno)s 指的日志级别的分数 debug-10, info-20, warning-30, error-40 and critical-50
        # %(module)s 03 writefileview(不带py)
        # %(msecs)s  指的是时间得毫秒
        # %(pathname)s  显示当前文件的绝对路径 # D:/PycharmProjects/s12/day6_0220/03 xiaojie/05 logging模块/03 writefileview.py-

        sh.setFormatter(formatter) #添加日志格式到屏幕句柄
        fh.setFormatter(formatter) #添加日志格式到文件句柄

        logger.addHandler(sh) #添加屏幕句柄到日志对象
        logger.addHandler(fh) #添加文件句柄到日志对象

        logger.debug('debug message')  #注意，这里是logger不能是logging，否则输出不对
        logger.info('info message')
        logger.warn('warn message')
        logger.error('error message')
        logger.critical('critical message')

#2添加用户方法，既可以添加警察，也可以添加土匪
    def add_user(self):
        break_flag =False
        while True:
            user_input = input("请输入需要添加的用户名:")
            # 1读出用户表到字典
            q_data_user = select("life","bbb")
            #2添加键值对到字典（用户名自定义输入，初始登录密码，初始余额，初始预算，初始错误登录次数,初始冻结状态，初始支付密码都给默认值）
            q_data_user[user_input] = {"bodyarmor": "True", "role": "police", "money": 15000, "weapon": "B22", "life_value": 100}
            print(q_data_user)
            #3将添加键值对后的字典，重新写入到文件json
            f = open("username1.txt","w") #新建一个新文件
        # f.seek(0)
            json.dump(q_data_user,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_user转换后写入f）
            f.close()
            print("\033[32;1m用户添加成功,新用户是[%s]，初始角色是[%s]，初始生命值是[%s]点，初始金币是[%s]元,初始武器是[%s],初始防弹衣是[%s]\033[0m" % (user_input,q_data_user[user_input]["role"],q_data_user[user_input]["life_value"],q_data_user[user_input]["money"],q_data_user[user_input]["weapon"],q_data_user[user_input]["bodyarmor"]))
            # break
            p1.log1()

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

#3对字典的键进行排序的方法

    def chushihua(arg1):  #arg1是形式参数  主模块mydic是实际参数传入（调用函数的时候，传入实参）
        #3对字典的键进行排序的方法
        arg1 = select("life","aaa")
        li_dickey=arg1.keys()   #将用户输入的字典的key添加到列表，无序的，无法通过索引号定位
        li_dickey = list(li_dickey)  #字典的key需要转换成list，才能排序
        li_dickey.sort()   #将列表排序后，通过索引号取出字典的key
        return li_dickey   #返回已经排序的列表

#4显示姓名、生命值等身份信息
    def view(self): #显示姓名、生命值等身份信息
        #1读出文件到字典
        q_data = select("life","aaa") #1读用户表
        # print(q_data)
        # #2打印字典的信息
        li_dickey=q_data.keys()   #将用户输入的字典的key添加到列表，无序的，无法通过索引号定位
        ret = list(li_dickey)  #字典的key需要转换成list，才能排序
        # print(ret)
        ret.sort()   #将列表排序后，通过索引号取出字典的key
        # print(ret)
         #单独采用‘%s’时，直接输出字符串，
#     # ‘%10s’表示在字符串前面添加占位符，并且字符串采用右对齐的方式，
#     # ‘%-10s’表示在字符串后面添加占位符(这10位占位符包含字符串)，字符串采用左对齐的方式。
#     #   例如字符串本身是"abc"3位，那么‘%-10s’表示在字符串"abc"后添加7位占位符
        # # ret = chushihua(q_data[user]) #将字典的键放在列表中，给列表排序
        # print("身份信息如下：")
        # print("您目前的角色是:",q_data[ret[0]]["role"])
        print ('%-9s%-9s%-9s%-9s%-9s' % ("角色","姓名", "武器","生命值", "金币"))
        print ('%-11s%-11s%-11s%-11s%-11s' % (q_data[ret[0]]["role"],ret[0], q_data[ret[0]]["weapon"],q_data[ret[0]]["life_value"], q_data[ret[0]]["money"]))
        # print ('%-11s%-11s%-11s%-11s' % (ret[1], q_data[user][ret[1]]["weapon"],q_data[user][ret[1]]["life_value"], q_data[user][ret[1]]["money"]))
        print ('%-11s%-11s%-11s%-11s%-11s' % (q_data[ret[1]]["role"],ret[1], q_data[ret[1]]["weapon"],q_data[ret[1]]["life_value"], q_data[ret[1]]["money"]))

#5发起攻击方法
    def shot(self): #方法（实例r1调用这个方法，self就是实例本身r1;实例r2调用这个方法，self就是实例本身r2）
        print("shooting...")

#6加血方法,形式参数user的实参是用户名:给哪个用户加血（调用的时候传入实参）
    def add_blood(self,user):
        q_data_life = select("life","ddd") #1读用户生命表
        life_value = q_data_life[user]["life_value"]  #用户的生命值
        q_data_life[user]["life_value"] +=10  #每次调用加血方法，回复10点生命值
        print("\033[32;1m加血，恢复10点生命值\033[0m")

          #3将修改后的用户生命值，写入文件
            #修改后的生命值写文件
        f = open("username1.txt","w") #新建一个新文件
        json.dump(q_data_life,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_life转换后写入f）
        f.close()

        #6加血后，新建一个历史记录表
            #构造字典，往字典添加键值对，写入到文件
        my_dic1 = {'name':user,'role':q_data_life[user]["role"],"ipaddr":ipaddr, 'life_value': 10,"type":"add_blood","time":time.strftime('%Y-%m-%d %H:%M:%S')}
        # print(my_dic1)

        j_str = json.dumps(my_dic1)  #先把字典转换成字符串
        f = open("addblood_his.txt","a")  #往原有的文件中追加取款记录
        f.write(j_str)   #再写入到文件
        f.write("\n")   #添加换行符  这里手动添加换行
        # f.write(data) #直接写入字典，报错 TypeError: write() argument must be str, not dict
        f.close()

        p1.add_blood_his(user)  #调用加血历史记录方法，前台显示

        # print("---加血历史记录---")
        # print ('%-20s%-20s%-9s%-9s%-9s%-9s' % ("时间","登录IP","用户","角色","操作类型", "生命值增加单位点"))
        # f  = open("addblood_his.txt","r")
        # for i in f:
        #     my_dic1 = json.loads(i)   #经过json.loads转换后，读取的字符串转换成了字典
        #     if user == my_dic1["name"]:  #根据用户名和传入的参数user比对，判断
        #         print ('%-22s%-22s%-11s%-11s%-14s%-9s' % (my_dic1["time"],ipaddr, my_dic1["name"],my_dic1["role"],my_dic1["type"], my_dic1["life_value"]))
        # p1.log1()

#7加血历史记录查看,形式参数user的实参是用户名:查看哪个用户的加血记录（调用的时候传入实参）
    def add_blood_his(self,user):
        print("---加血历史记录---")
        print ('%-20s%-20s%-9s%-9s%-9s' % ("时间","登录IP", "用户","操作类型", "生命值增加单位点"))
        f  = open("addblood_his.txt","r")
        for i in f:
            my_dic1 = json.loads(i)   #经过json.loads转换后，读取的字符串转换成了字典
            if user == my_dic1["name"]:  #根据用户名和传入的参数user比对，判断
                print ('%-22s%-22s%-11s%-14s%-9s' % (my_dic1["time"],ipaddr, my_dic1["name"],my_dic1["type"], my_dic1["life_value"]))
#8受到攻击，减血的方法

    def got_shot(self,user,arg1):
        # print("I got shot...")
        # 8受到攻击，减血的方法，参数user的实参是用户名:哪个用户受到了攻击；参数arg1的实参是武器：挨打者是受到了哪种武器的打击
        q_data_life = select("life","ddd") #1读用户生命表
        q_data_weapons = select("weapons","ddd") #1读用户武器表
        # print(q_data_life)
        # print(q_data_weapons)
        life_value = q_data_life[user]["life_value"]  #用户的生命值
        # print(q_data_life[user]["life_value"])
        # print(q_data_weapons[user]["1"]["goods"])  #用户的武器
        if life_value>0:
            # life_value -=10  #这里有个坑，如果是life_value-=10就会出现生命值不变的情况，需要用q_data_life[user]["life_value"] -=10才行
            if random.randrange(1,4) == random.randrange(1,3):
                print("\033[32;1m哈哈,没有命中，对方没有掉血\033[0m")
            else:
                if q_data_life[user]["bodyarmor"] == "False": #and q_data_weapons[user]["1"]["goods"]=="Ak47":  #没有防弹衣每次中枪，伤害是10
                    if arg1 == q_data_weapons[user]["1"]["goods"]:
                        q_data_life[user]["life_value"] -=int(q_data_weapons[user]["1"]["hurt"])  #2修改用户生命值
                        # print(q_data_life[user]["life_value"])
                        # print(int(q_data_weapons[user]["1"]["hurt"]))
                        print("\033[32;1m对方无防弹衣，被[%s]击中,掉血,生命值减10点\033[0m" % q_data_weapons[user]["1"]["goods"] )
                    elif arg1 == q_data_weapons[user]["2"]["goods"]:
                        q_data_life[user]["life_value"] -=int(q_data_weapons[user]["2"]["hurt"])  #2修改用户生命值
                        print("\033[32;1m对方无防弹衣，被[%s]击中,掉血,生命值减20点\033[0m"% q_data_weapons[user]["2"]["goods"])
                    elif arg1 == q_data_weapons[user]["3"]["goods"]:
                        q_data_life[user]["life_value"] -=int(q_data_weapons[user]["3"]["hurt"])  #2修改用户生命值
                        print("\033[32;1m对方无防弹衣，被[%s]击中，掉血,生命值减30点\033[0m"% q_data_weapons[user]["3"]["goods"])
                    elif arg1 == q_data_weapons[user]["4"]["goods"]:
                        q_data_life[user]["life_value"] -=int(q_data_weapons[user]["4"]["hurt"])  #2修改用户生命值
                        print("\033[32;1m对方无防弹衣，被[%s]击中，掉血,生命值减40点\033[0m"% q_data_weapons[user]["4"]["goods"])
                    else:
                        print("\033[31;1m程序中武器的单词和文件中武器的单次不一致，请检查\033[0m")
                if q_data_life[user]["bodyarmor"] == "True":  #有防弹衣，每次中枪，伤害是5
                    if arg1 == q_data_weapons[user]["1"]["goods"]:
                        q_data_life[user]["life_value"] -=int(q_data_weapons[user]["1"]["hurt"])/2  #2修改用户生命值
                        print("\033[32;1m对方有防弹衣，被[%s]击中,损伤减半，掉血,生命值减5点\033[0m"% q_data_weapons[user]["1"]["goods"])
                    elif arg1 == q_data_weapons[user]["2"]["goods"]:
                        q_data_life[user]["life_value"] -=int(q_data_weapons[user]["2"]["hurt"])/2  #2修改用户生命值
                        print("\033[32;1m对方有防弹衣，被[%s]击中,损伤减半，掉血,生命值减10点\033[0m"% q_data_weapons[user]["2"]["goods"])
                    elif arg1 == q_data_weapons[user]["3"]["goods"]:
                        q_data_life[user]["life_value"] -=int(q_data_weapons[user]["3"]["hurt"])/2  #2修改用户生命值
                        print("\033[32;1m对方有防弹衣，被[%s]击中，损伤减半，掉血,生命值减15点\033[0m"% q_data_weapons[user]["3"]["goods"])
                    elif arg1 == q_data_weapons[user]["4"]["goods"]:
                        q_data_life[user]["life_value"] -=int(q_data_weapons[user]["4"]["hurt"])/2  #2修改用户生命值
                        print("\033[32;1m对方有防弹衣，被[%s]击中，损伤减半，掉血,生命值减20点\033[0m"% q_data_weapons[user]["4"]["goods"])
                    else:
                        print("\033[31;1m程序中武器的单词和文件中武器的单次不一致，请检查\033[0m")
        else:
            print("\033[31;1m对方的生命值小于等于0，挂了，游戏结束,是否退出游戏\033[0m")
        #3将修改后的用户生命值，写入文件
            #修改后的生命值写文件
        f = open("username1.txt","w") #新建一个新文件
        json.dump(q_data_life,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_life转换后写入f）
        f.close()
        # p1.log1()  #通过实例调标准日志方法

#9购买武器枪支的方法，参数user的实参是用户名：哪个用户购买武器
    def buy_gun(self, user):
        # print("%s just bought %s" % (self.name,gun_name))
        total =0 #定义武器一共多少钱
        q_data = select("shop","ddd")  #1读武器表
        # print(q_data)  #{'1': {'price': 6099, 'goods': 'iphone6s', 'times': 0}, '2': {'price': 8888, 'goods': 'mac', 'times': 0}}
        q_data_yue = select("life","ddd") #2读用户生命值表
        # print(q_data_yue) #{'jack': {'yue': 15000, 'yusuan': 15000}}
        # num = q_data_yue[user]["yusuan"]   #定义购物预算（兜里一共多少钱） 预算可以直接定义，也可以从文件中读取
        num =150000
        yue = q_data_yue[user]["money"]  #用户的余额
        break_flag = False  #跳出外循环标识

        li_dickey=q_data[user].keys()   #将用户输入的字典的key添加到列表，无序的，无法通过索引号定位
        ret = list(li_dickey)  #字典的key需要转换成list，才能排序
        ret.sort()   #将列表排序后，通过索引号取出字典的key

        # ret = chushihua(q_data[user]) #将字典的键放在列表中，给列表排序
        q_data[user][ret[0]]["times"] = 0 #每次购买前，先将购买数量置为0
        q_data[user][ret[1]]["times"] = 0 #如果不将购买数量置为0，就是个累计效应

        #3修改购买数量和余额
        while True: #外循环，输入商品编号
            print("----欢迎购买武器，提高战斗力----")
            print("---武器编号列表---")
            print ('%-7s%-7s%-7s%-7s' % ("武器编号", "武器名称","武器价格", "购买数量"))
            print ('%-11s%-11s%-11s%-11s' % (ret[0], q_data[user][ret[0]]["goods"],q_data[user][ret[0]]["price"], q_data[user][ret[0]]["times"]))
            print ('%-11s%-11s%-11s%-11s' % (ret[1], q_data[user][ret[1]]["goods"],q_data[user][ret[1]]["price"], q_data[user][ret[1]]["times"]))
            # #打印商品编号列表
            print("您的余额目前是%s元" % q_data_yue[user]["money"])
            yue_before = q_data_yue[user]["money"]
            goods_no_input = input("请输入你要买的商品编号:") #要求用户输入商品编号
            if len(goods_no_input)==0: #如果商品编号为空
                print("\033[31;1m商品编号不能为空\033[0m")
            elif goods_no_input not in q_data[user]: #如果商品编号不存在
                print("\033[31;1m商品编号不存在\033[0m")
            else: #商品编号存在(调支付接口),下面的支付结算单独成一个函数，支付密码验证用装饰器
                # print(ret[0],total)
                if  total < num and yue>q_data[user][goods_no_input]["price"]: #bug修复，当商品总价格超过用户预算的时候，就不要再累加商品价格了，否则会出现98行，余额是负数的情况
                    total += q_data[user][goods_no_input]["price"]  #累加商品的价格（需要支付多少钱）
                # print(ret[1],total)
                # # 先计算商品总价格，在将商品这价格和预算比对
                if total < num and yue>q_data[user][goods_no_input]["price"]: #如果需要支付的钱小于用户的预算
                    q_data[user][goods_no_input]["times"] += 1  #购买数量+1
                    # print("3",q_data_yue["jack"]["yue"])
                    # q_data_yue["jack"]["yue"] -= total
                    q_data_yue[user]["money"] -= q_data[user][goods_no_input]["price"]    #关键点：原始的余额是10000文件中，每买一件商品，余额扣减商品的价格
                    #这里必须将total改成shop_dict[goods_no_input]["price"]  否则逻辑不对
                    # print("4",q_data_yue["jack"]["yue"])
                    # yue_list[-1] = num - total   #用户预算扣除购物车的花费后，计算用户的余额
                    # print("已经放入购物车，输入x，继续购物；输入y，去结算，请输入支付密码结算")
                    while True:
                        jiesuan = input("输入y，去结算；输入a，继续购买:")
                        if jiesuan == "y":
                            # login(user)  #调支付密码验证函数,这里需要将注册后输入的用户名作为参数传入
                            break  #跳出循环的当前迭代，回到75行
                        elif jiesuan == "a":
                            # break_flag = True  #外循环跳出标签
                            break
                        else:  #如果输入的不是x或者y
                            print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
                            continue  #跳出内循环本次迭代

                    print("\033[32;1m目前没有超出预算，当前余额是%s元,可以继续购买,输入c，退出程序；输入a，继续购买:\033[0m:" % q_data_yue[user]["money"])
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
                    print("\033[31;1m钱不够了,当前余额是%s元，想要买这件商品，还差%s元\033[0m" % (q_data_yue[user]["money"],q_data[user][goods_no_input]["price"]-yue))

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
                            # addblood_his.txt()
                        else:  #如果输入的不是q或者b
                            print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
                            continue  #跳出内循环本次迭代
                    if break_flag:
                        break  #跳出外循环

        f = open("shop_gun.txt","w") #新建一个新文件
        # f.seek(0)  #回到文件最开始
        json.dump(q_data,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data转换后写入f）
        f.close()

        #5修改后的余额写文件
        f = open("username1.txt","w") #新建一个新文件
        # f.seek(0)
        json.dump(q_data_yue,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_yue转换后写入f）
        f.close()

        #5打印买枪清单和余额（累计）
        print("---购物清单---")
        print ('%-7s%-7s%-7s%-7s%-7s' % ("武器编号", "武器名称","武器价格", "购买数量","购买用户"))
        print ('%-11s%-11s%-11s%-11s%-11s' % (ret[0], q_data[user][ret[0]]["goods"],q_data[user][ret[0]]["price"], q_data[user][ret[0]]["times"],user))
        print ('%-11s%-11s%-11s%-11s%-11s' % (ret[1], q_data[user][ret[1]]["goods"],q_data[user][ret[1]]["price"], q_data[user][ret[1]]["times"],user))
        print("您的余额目前是%s元" % q_data_yue[user]["money"])
        yue_after = q_data_yue[user]["money"]

        #6买枪结算后，新建一个历史记录表
            #构造字典，往字典添加键值对，写入到文件
        my_dic1 = {'name':user,"ipaddr":ipaddr, 'money': yue_before-yue_after,"type":"buy_gun","time":time.strftime('%Y-%m-%d %H:%M:%S')}
        # print(my_dic1)

        j_str = json.dumps(my_dic1)  #先把字典转换成字符串
        f = open("buygun_his.txt","a")  #往原有的文件中追加取款记录
        f.write(j_str)   #再写入到文件
        f.write("\n")   #添加换行符  这里手动添加换行
        # f.write(data) #直接写入字典，报错 TypeError: write() argument must be str, not dict
        f.close()

        #7打印单次购物记录-时间 地点 人物 事件（每次购物结算时花了多少）
        p1.buy_gun_his(user)  #调用购买武器历史记录方法，前台显示
        # print("---买枪交易历史记录---")
        # print ('%-20s%-20s%-9s%-9s%-9s' % ("时间","登录IP", "用户","交易类型", "消费金额单位元"))
        # f  = open("buygun_his.txt","r")
        # for i in f:
        #     my_dic1 = json.loads(i)   #经过json.loads转换后，读取的字符串转换成了字典
        #     if user == my_dic1["name"]:  #根据用户名和传入的参数user比对，判断
        #         print ('%-22s%-22s%-11s%-14s%-9s' % (my_dic1["time"],ipaddr, my_dic1["name"],my_dic1["type"], my_dic1["money"]))


#9购买武器枪支的历史记录查看

    def buy_gun_his(self,user):
        pass #10购买武器枪支的历史记录查看 参数user的实参是用户名：哪个用户要查看购买武器记录
        print("---买枪交易历史记录---")
        print ('%-20s%-20s%-9s%-9s%-9s' % ("时间","登录IP", "用户","交易类型", "消费金额单位元"))
        f  = open("buygun_his.txt","r")
        for i in f:
            my_dic1 = json.loads(i)   #经过json.loads转换后，读取的字符串转换成了字典
            if user == my_dic1["name"]:  #根据用户名和传入的参数user比对，判断
                print ('%-22s%-22s%-11s%-14s%-9s' % (my_dic1["time"],ipaddr, my_dic1["name"],my_dic1["type"], my_dic1["money"]))

    #11 增加金币方法
    def add_money(self,user):
        """
        :param user: 给哪个用户加金币
        :return:
        """
        q_data_money = select("life","money") #1读用户生命表
        money = q_data_money[user]["money"]  #用户的金币
        q_data_money[user]["money"] +=10  #每次调用加金币方法，增加10个金币
        print("\033[32;1m加金币，增加10个金币\033[0m")

          #3将修改后的用户金币值，写入文件
            #修改后的生命值写文件
        f = open("username1.txt","w") #新建一个新文件
        json.dump(q_data_money,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_life转换后写入f）
        f.close()

        #6加金币后，新建一个历史记录表
            #构造字典，往字典添加键值对，写入到文件
        my_dic1 = {'name':user,'role':q_data_money[user]["role"],"ipaddr":ipaddr, 'money': 10,"type":"add_money","time":time.strftime('%Y-%m-%d %H:%M:%S')}
        # print(my_dic1)

        j_str = json.dumps(my_dic1)  #先把字典转换成字符串
        f = open("addmoney_his.txt","a")  #往原有的文件中追加加钱记录
        f.write(j_str)   #再写入到文件
        f.write("\n")   #添加换行符  这里手动添加换行
        # f.write(data) #直接写入字典，报错 TypeError: write() argument must be str, not dict
        f.close()

        p1.add_money_his(user) #调用增加金币历史记录方法，前台显示

    #12 增加金币历史记录
    def add_money_his(self,user):
        print("---加金币历史记录---")
        print ('%-20s%-20s%-9s%-9s%-9s%-9s' % ("时间","登录IP","用户","角色","操作类型", "金币增加单位个"))
        f  = open("addmoney_his.txt","r")
        for i in f:
            my_dic1 = json.loads(i)   #经过json.loads转换后，读取的字符串转换成了字典
            if user == my_dic1["name"]:  #根据用户名和传入的参数user比对，判断
                print ('%-22s%-22s%-11s%-11s%-14s%-9s' % (my_dic1["time"],ipaddr, my_dic1["name"],my_dic1["role"],my_dic1["type"], my_dic1["money"]))
        # p1.log1()

class Police(Role):
    def __init__(self,name,role,weapon,bodyarmor,life_value =100,money=15000):
        super(Police,self).__init__(name,role,weapon,life_value =100,money=15000)
        self.bodyarmor = bodyarmor  #是否穿防弹衣  是true否false

    def rescue_hostages(self): #保护人质方法
        print("别怕，我是警察，我来救你了")
        return True


class Terrorist(Role):
    def __init__(self,name,role,weapon,masked,life_value =100,money=15000):
        super(Terrorist,self).__init__(name,role,weapon,life_value =100,money=15000)
        self.masked = masked  #是否蒙面  是true否false

    def kill_hostages(self): #杀害人质方法
        print("我是恐怖分子，我有人质在手，3天内交50万美金赎人，否则，撕票")

    def add_user(self):  #重写父类中的添加用户的方法
        break_flag =False
        while True:
            user_input = input("请输入需要添加的用户名:")
            # 1读出用户表到字典
            q_data_user = select("life","bbb")
            #2添加键值对到字典（用户名自定义输入，初始登录密码，初始余额，初始预算，初始错误登录次数,初始冻结状态，初始支付密码都给默认值）
            q_data_user[user_input] = {"bodyarmor": "False", "role": "terrorist", "money": 15000, "weapon": "B22", "life_value": 100,"masked": "False"}
            print(q_data_user)
            #3将添加键值对后的字典，重新写入到文件json
            f = open("username1.txt","w") #新建一个新文件
        # f.seek(0)
            json.dump(q_data_user,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_user转换后写入f）
            f.close()
            print("\033[32;1m用户添加成功,新用户是[%s]，初始角色是[%s]，初始生命值是[%s]点，初始金币是[%s]元,初始武器是[%s],初始防弹衣是[%s]\033[0m" % (user_input,q_data_user[user_input]["role"],q_data_user[user_input]["life_value"],q_data_user[user_input]["money"],q_data_user[user_input]["weapon"],q_data_user[user_input]["bodyarmor"]))
            # break

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

p1 = Police("jack","police","B22","False") #新建一个警察实例
t1 = Terrorist("tom","terrorist","Ak47","False") #新建一个土匪实例

