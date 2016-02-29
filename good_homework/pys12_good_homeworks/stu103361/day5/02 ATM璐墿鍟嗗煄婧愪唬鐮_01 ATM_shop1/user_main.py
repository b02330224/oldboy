__author__ = 'Administrator'
#-*- coding:utf-8 -*-
import sys
# print(sys.path)  #默认路径是当前py文件的父目录

import json
from backend.db.sql_api import select



#跨目录结构--导入包 init  backend是user_mian的同级目录
from backend.logic  import gouwuche   #可以正常导入执行，只是pycharn没有认识backend而已。不影响导入
#从模块backend.logic导入模块handles.py

if __name__ == "__main__":
    break_flag = False
    q_data_dic = select("username","bbb")
    key1 = q_data_dic.keys()
    while True:
        print ("---欢迎使用程序---")
        print ("=================")
        print ('%-8s' % ("购物商城[a]"))
        print ('%-8s' % ("ATM[b]"))
        print ('%-8s' % ("管理接口[c]"))
        print ('%-8s' % ("退出程序[d]"))
        print ("=================")
        rukou = input("请选择操作:")

        if rukou == "a":
            print("欢迎使用购物商城")
            while True:
                user= input("目前已经注册的用户是[%s],请输入你要登录购物商城的用户:" % key1)
                if user in q_data_dic and q_data_dic[user]["status"]!="inactive":
                # if user == "jack" or user =="tom":
                    print ('%-14s%-14s' % ("购物[a]","购物历史记录查询[b]"))
                    rukou2 = input("请选择操作:")
                    # rukou2 = input("欢迎使用ATM，输入a，充值；输入b，转账；输入c，查询余额；输入d，取款;输入e，调整预算;输入f，修改登录密码;输入g，退出程序;输入h，修改支付密码:")
                    # break_flag = True  #外循环跳出标签
                    if rukou2 == "a":
                        gouwuche.home(user)  #welcome  to home page
                        break_flag = True
                        break
                    elif rukou2 == "b":
                        gouwuche.gouwu_his(user)  #welcome  to home page
                        # break_flag = True
                        break
                    else:  #如果输入的不是a或者b
                        print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
                        continue  #跳出内循环本次迭代
                elif user in q_data_dic and q_data_dic[user]["status"]=="inactive":
                    print("\033[31;1m对不起，该用户已经冻结不可用，请联系管理员先解冻该用户\033[0m")
                    continue
                else:
                    print("\033[31;1m对不起，你输入的用户还没有注册，无法登录购物商城，请重新输入\033[0m")
                    continue  #跳出循环的当前迭代，回到75行
            if break_flag:
                break
        elif rukou == "b":
            print("欢迎使用ATM")
            while True:
                # key1 = q_data_dic.keys()
                user= input("目前已经注册的用户是[%s],请输入你要登录ATM的用户:" % key1)
                if user in q_data_dic and q_data_dic[user]["status"]!="inactive":
                # if user == "jack" or user =="tom":
                    gouwuche.Login(user)  #验证登录接口
                    # continue  #跳出循环的当前迭代，回到75行
                elif user in q_data_dic and q_data_dic[user]["status"]=="inactive":
                    print("\033[31;1m对不起，该用户已经冻结不可用，请联系管理员先解冻该用户\033[0m")
                    continue
                else:
                    print("\033[31;1m对不起，你输入的用户还没有注册，无法登录ATM，请重新输入\033[0m")
                    continue
                print ("---欢迎使用ATM---")
                print ("=================")
                print ('%-18s%-14s' % ("充值[a]","调整预算[e]"))
                print ('%-18s%-14s' % ("转账[b]","修改登录密码[f]"))
                print ('%-16s%-14s' % ("查询余额[c]","退出程序[g]"))
                print ('%-18s%-14s' % ("取款[d]","修改支付密码[h]"))
                print ('%-18s%-14s' % ("提现[j]","ATM操作日志查询[i]"))
                print ("=================")
                rukou2 = input("请选择操作:")
                # rukou2 = input("欢迎使用ATM，输入a，充值；输入b，转账；输入c，查询余额；输入d，取款;输入e，调整预算;输入f，修改登录密码;输入g，退出程序;输入h，修改支付密码:")
                # break_flag = True  #外循环跳出标签
                if rukou2 == "a":
                    gouwuche.chongzhi(user)
                    # gouwuche.chongzhi_jilu(user)
                    # gouwuche.chongzhi_jilu_view(user)
                    break  #跳出循环的当前迭代，回到75行
                    # else:
                    #     print("\033[31;1m对不起，你输入的用户还没有注册，无法登录ATM，请重新输入\033[0m")
                elif rukou2 == "b":
                    gouwuche.zhuanzhang(user)
                    # break_flag = True  #外循环跳出标签
                    break
                elif rukou2 == "c":
                    gouwuche.chaxunyue(user)
                    break
                elif rukou2 == "d":
                    gouwuche.qukuan(user)
                    break
                elif rukou2 == "e":
                    gouwuche.yusuan(user)
                    break
                elif rukou2 == "f":
                    gouwuche.xiugaimima(user)
                    break
                elif rukou2 == "g":
                    break_flag= True
                    break
                elif rukou2 == "h":
                    gouwuche.xiugaimima_zf(user)
                    break
                elif rukou2 == "i":
                    gouwuche.history_ATM(user)
                    break
                elif rukou2 == "j":
                    gouwuche.tixian(user)
                    break
                else:  #如果输入的不是a或者c
                    print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
                    continue  #跳出内循环本次迭代
            if break_flag:
                break
        elif rukou == "c":
            while True:
                print ("---欢迎使用管理接口---")
                print ("=================")
                print ('%-14s%-14s' % ("添加用户[a]","解冻用户[e]"))
                print ('%-14s%-14s' % ("删除用户[b]","回到上一级[f]"))
                print ('%-14s%-14s' % ("查询用户[c]","退出程序[g]"))
                print ('%-14s' % ("冻结用户[d]"))
                print ("=================")
                zhiling = input("请选择操作:")
                # zhiling= input("欢迎使用管理接口，输入a，进入添加用户；输入b，进入删除用户；输入c，进入查询用户；输入d，进入冻结用户；输入e，进入解冻用户；输入f，回到上一级；输入g，退出程序;目前已经注册的用户是[%s]:" % key1)
                if zhiling == "a":
                    gouwuche.adduser()
                    break
                elif zhiling == "b":
                    gouwuche.deluser()
                    break
                elif zhiling == "c":
                    gouwuche.viewuser()
                    break
                elif zhiling == "d":
                    gouwuche.inactiveuser()
                    break
                elif zhiling == "e":
                    gouwuche.activeuser()
                    break
                elif zhiling == "f":
                    break
                elif zhiling == "g":
                    break_flag = True
                    break
                else:  #如果输入的不是a或者c
                    print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
                    continue
            if break_flag:
                break
        elif rukou == "d":
            break
        else:  #如果输入的不是a或者b
            print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
            continue  #跳出内循环本次迭代

# readme
# 1、功能描述
#    1、分为购物商城、ATM、管理接口一共3个大的模块
#    2、购物商城分为购物和购物历史记录查询2个模块
#       1、购物支持买东西加入购物车，调用信用卡支付接口结账（调支付密码结账），购物商城支持多用户登录
# 	    （调用登录接口通过装饰器实现，通过修改用户表的错误登录次数实现3次登录错误锁定功能）
# 	     1、支付接口主要是：修改用户表中的余额字段，修改商品表中的购物数量
# 	  2、购物历史记录查询（信用卡对账单）支持最近30天的消费流水记录
# 	     1、购物历史记录：主要是每次购买记录往购物历史记录文件中新增加一个字典，每个字典一行
# 	      打印购买操作日志的时候，就一行一行像读取文件一样读取字典，json转换后变成字典处理，得到
# 		  时间、地点（登录IP）、人物（用户名）、事件（交易类型、交易金额）等操作日志要素
#    3、ATM分为充值、调整预算（额度）、转账、修改登录密码、查询余额、取款、修改支付密码、提现、ATM操作日志查询一共9个小模块
#       1、登录ATM通过调用登录接口实现用户名密码验证，这里ATM和购物商城的用户是同一套，没有分开，类似于支付宝和淘宝
# 	  2、登录前还支持判断用户是否注册，已经用户的可以状态是否是冻结(冻结的账户不能登录)
# 	  3、充值：修改用户表中的余额字段，增加余额（通过json实现文件的读写）
# 	  4、转账：用户表中转出方的余额减少，收款人的余额增加
# 	  5、取款：修改用户表中的余额字段，减少余额
# 	  6、提现：修改用户表中的余额（额度）字段，减少余额，同时加上提现手续费
# 	  7、查询余额：读取用户表中的余额字段
# 	  8、调整额度：修改用户表中的信用卡额度字段
# 	  9、修改登录密码：修改用户表中的登录密码字段
# 	  10、修改支付密码：修改用户表中的支付密码字段
# 	  11、ATM操作日志查询：上述充值、转账、提现等每一笔操作，都往atm历史记录文件中新增加一个字典，每个字典一行
# 	      打印操作日志的时候，就一行一行像读取文件一样读取字典，json转换后变成字典处理，得到
# 		  时间、地点（登录IP）、人物（用户名）、事件（交易类型、交易金额）等操作日志要素
# 	4、管理接口分为添加用户、删除用户、查询用户信息、冻结用户、解冻用户一共5个小的模块
# 	   1、添加用户：给用户表的字典新增加一个键值对，键值对中包含用户信息（用户名、登录密码、支付密码、余额、额度、冻结状态等信息）
# 	   2、删除用户：给用户表的字典删除指定的键值对
# 	   3、查询用户信息：读取用户表中指定用户的信息
# 	   4、冻结用户：修改用户表中指定用户的状态status为inactive（冻结状态）
#        5、解冻用户：修改用户表中指定用户的状态status为active（可用状态）
# 2、代码结构介绍
#    1、主函数：user_main.py，调后套逻辑函数
#    2、后台逻辑函数logic：gouwuche.py 购物商城、ATM、管理接口3大模块的功能函数都在这个文件中
#    3、db数据库接口层：sql_api.py  读取文件，将文件中的字典转换成字典格式，提供给logic功能函数使用
#    4、配置层：settings.py  定义数据库的连接信息（目前只用到文件，只是验证了数据库的登录操作，后续从文件过度到数据库使用）
#    5、文件中--表数据结构
#       1、用户表-username1.txt：用户名、登录密码、支付密码、余额、额度、冻结状态、错误登陆次数等信息
# 	  2、商品明细表-shop.txt：用户名、商品编号、商品名称、商品价格、购买数量等商品信息
# 	  3、ATM操作历史记录表-chongzhi.txt：时间、登录IP、用户、交易类型、交易金额等操作信息
# 	  4、购物历史流水表-gouwu_his.txt：时间、登录IP、用户、交易类型、消费金额等购买结算信息
# 3、整体思路
# 4、踩过的坑
#    1、问题现象：连续多次充值，只记录了最后一次充值记录、用户的余额是对的，已经写入文件了，就是充值记录值记录了最后一次--ok
#       原因分析：因为分成了2个函数，1个充值函数专门用来处理余额的变动，另外1个充值函数专门处理新增加充值记录，打印充值记录
#                充值记录函数需要调用充值函数，显示充值金额，但是充值函数只有在退出的时候return，无法在多次充值的时候return充值金额
#       解决办法：将充值记录函数合并到充值函数，就可以直接调用充值金额，不需要充值函数return了
#    2、问题现象：ATM操作历史记录表和购物历史流水表：每一笔操作，都往历史记录文件中新增加一个字典，但是所有的字典都在同一行
#                会导致单个字典记录无法读取出来，无法打印日志记录
# 	  解决办法：dumps+手写换行符的方式，而不是dump的方式，这样每个字典一行，像处理文件一样一行行读取，读一行把内容json.loads一下，就是字典
# 	  j_str = json.dumps(my_dic1)  #先把字典转换成字符串
#         f = open("chongzhi.txt","a")  #a模式、追加内容到文件最后
#         f.write(j_str)   #再写入到文件
#         f.write("\n")   #添加换行符  这里手动添加换行
#         # f.write(data) #直接写入字典，报错 TypeError: write() argument must be str, not dict
#         f.close()
#
#         # f = open("chongzhi.txt","a") #新建一个新文件
#         # # f.seek(0)
#         # json.dump(my_dic1,f)   #将字典通过json.dump转换成字符串，并且同时写入到文件（将字典q_data_yue转换后写入f）
#         # f.close()
# 5、涉及的知识点
#    1、通过json(loads/dump)读写文件中的数据（文件中字典的形式组织存储数据）
#       1、json修改字典中字段
# 	  2、添加删除键值对
# 	  3、计算月还款总额：用到将字典的value依次添加到列表中，然后计算列表各个元素的和sum函数
# 	  4、打印商品列表：用到将字典的key商品编号，依次添加到列表后，排序后，通过列表索引号指定商品标号
# 	  5、ATM操作历史记录表和购物历史流水表：每一笔操作，都往历史记录文件中新增加一个字典，每个字典一行（dumps+手写换行符的方式，而不是dump的方式）
# 	      打印操作日志的时候，就一行一行像读取文件一样读取字典，json转换后变成字典处理，得到
# 		  时间、地点（登录IP）、人物（用户名）、事件（交易类型、交易金额）等操作日志要素
#    2、主函数、逻辑函数、数据接口、配置文件的模块导入功能
#    3、socket得到ip地址：ipaddr = socket.gethostbyname(socket.gethostname())
#    4、计算账单的开始时间和结束时间的账期时候，用到datetime和time模块的时间转换（时间戳、结构时间、格式化时间得互相转换）
#    5、带参数的装饰器：购物商城的登录用到了装饰器；ATM的登录没有用到装饰器，是内部再次调用了登录接口；购物商城的支付密码单独调用了支付密码验证接口
#       优化方向：可以考虑购物商城和ATM都用带参数的装饰器实现
