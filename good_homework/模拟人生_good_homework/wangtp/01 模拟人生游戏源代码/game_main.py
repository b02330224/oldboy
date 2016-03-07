__author__ = 'Administrator'
#-*- coding:utf-8 -*-
import sys
# print(sys.path)  #默认路径是当前py文件的父目录

import json
import time
import random
from backend.db.sql_api import select


#跨目录结构--导入包 init  backend是user_mian的同级目录
from backend.logic  import game_logic   #可以正常导入执行，只是pycharn没有认识backend而已。不影响导入
#从模块backend.logic导入模块handles.py

if __name__ == "__main__":
     # print(random.randrange(1,4)) # 2 #随机输出整数，整数的范围1<=x<4(左闭右开)
     ret = game_logic.t1.chushihua()  #对用户表中字典的键进行排序
     # print(ret)
     while True:
        print ("---欢迎使用反恐精英CS单挑版游戏---")
        print ("=================")
        print ('%-8s' % ("警察[a]"))
        print ('%-8s' % ("土匪[b]"))
        print ('%-8s' % ("退出游戏[a、b之外其他字符]"))
        print ("=================")
        choice = input("请选择角色:")

        if choice == "a":
            print("\033[32;1m您目前的角色是:[%s] ；敌方角色是：[%s]\033[0m" % (game_logic.p1.role,game_logic.t1.role))
            print("目前双方生命值如下:")
            game_logic.p1.view()
            while True:
                print ('%-8s' % ("开战PK[c]"))
                print ('%-8s' % ("加血[d]"))
                print ('%-8s' % ("添加用户[e]"))
                print ('%-8s' % ("买枪[f]"))
                print ('%-18s' % ("买枪历史记录查询[g]"))
                print ('%-18s' % ("加血历史记录查询[h]"))
                print ('%-18s' % ("加金币历史记录查询[j]"))
                print ('%-18s' % ("解救人质[i]"))
                print ('%-8s' % ("回到上一级[cdefgh之外其他字符]"))
                menu_dic = {"e":game_logic.p1.add_user,"g":game_logic.p1.buy_gun_his,"h":game_logic.p1.add_blood_his,"j":game_logic.p1.add_money_his}  #当每个分支只调用单一方法，且不带参数的时候，这个方法很简洁
                choice2 = input("请选择操作:")
                if choice2 in menu_dic:
                    if choice2 == "e":
                        menu_dic[choice2]()
                    else:
                        menu_dic[choice2](ret[0])
                    continue
                elif choice2 == "c":
                #警察开枪击中恐怖分子，恐怖分子掉血
                    print("1-2秒后，[%s]就投入战斗了。。。" % game_logic.p1.role)
                    time.sleep(random.randrange(1,3))
                    print("[%s]对[%s]发起攻击" % (game_logic.p1.role,game_logic.t1.role))
                    game_logic.p1.shot()  #shooting...
                   # ret = game_logic.t1.chushihua()
                    random1 = random.randrange(1,5)  #随机调用下述4种武器，从1-4伤害值依次是10,20,30,40
                    dic = {1:"B11",2:"dagger",3:"sniper",4:"antitank_grenade"}
                    print(dic[random1])
                    game_logic.t1.got_shot(ret[1],dic[random1])
                    print("目前双方生命值如下:")
                    game_logic.p1.view()
                    # game_logic.p1.log1()
                    print("\033[32;1m本回合枪战结束，下一轮\033[0m")
                    continue
                elif choice2 == "d":
                    game_logic.p1.add_blood(ret[0])
                    game_logic.p1.view()
                    continue
                # elif choice2 == "e":
                #     game_logic.p1.add_user()
                #     continue
                elif choice2 == "f":
                    game_logic.p1.buy_gun(ret[0])
                    continue
                # elif choice2 == "g":
                #     game_logic.p1.buy_gun_his(ret[0])
                #     continue
                # elif choice2 == "h":
                #     game_logic.p1.add_blood_his(ret[0])
                #     continue
                elif choice2 == "i":
                    if game_logic.p1.rescue_hostages() == True:
                        print("人质解救成功")
                        game_logic.p1.add_money(ret[0])
                    continue
                else:
                    break
        elif choice == "b":
            print("\033[32;1m您目前的角色是: [%s]；敌方角色是：[%s]\033[0m" % (game_logic.t1.role,game_logic.p1.role))
            print("目前双方生命值如下:")
            game_logic.t1.view()
            while True:
                print ('%-8s' % ("开战[c]"))
                print ('%-8s' % ("加血[d]"))
                print ('%-8s' % ("添加用户[e]"))
                print ('%-8s' % ("买枪[f]"))
                print ('%-18s' % ("买枪历史记录查询[g]"))
                print ('%-18s' % ("加血历史记录查询[h]"))
                print ('%-8s' % ("回到上一级[cdefgh之外其他字符]"))
                choice2 = input("请选择操作:")
                if choice2 == "c":
                    print("1-2秒后，[%s]就投入战斗了。。。" % game_logic.t1.role)
                    time.sleep(random.randrange(1,3))
                #恐怖分子开枪击中警察，警察掉血
                    print("[%s]对[%s]发起攻击" % (game_logic.t1.role,game_logic.p1.role))
                    game_logic.t1.shot()  #shooting...
                    # ret = game_logic.t1.chushihua()
                    # game_logic.t1.got_shot(ret[0])
                    random2 = random.randrange(1,5)  #随机调用下述4种武器，从1-4伤害值依次是10,20,30,40
                    dic = {1:"AK47",2:"Rifle",3:"sniper",4:"rocket_gun"}
                    print(dic[random2])
                    game_logic.t1.got_shot(ret[0],dic[random2])
                    # game_logic.p1.got_shot("jack")
                    game_logic.t1.view()
                    print("\033[32;1m本回合枪战结束，下一轮\033[0m")
                    continue
                elif choice2 == "d":
                    game_logic.t1.add_blood(ret[1])
                    game_logic.t1.view()
                    continue
                elif choice2 == "e":
                    game_logic.t1.add_user()
                    continue
                elif choice2 == "f":
                    game_logic.t1.buy_gun(ret[1])
                    continue
                elif choice2 == "g":
                    game_logic.t1.buy_gun_his(ret[1])
                    continue
                elif choice2 == "h":
                    game_logic.t1.add_blood_his(ret[1])
                    continue
                else:
                    break
        else:
            print("\033[32;1m退出游戏\033[0m")
            break

# 1、代码结构介绍
#    1、主函数：game_main.py，调后台逻辑函数
#    2、后台逻辑函数：game_logic.py 公共类、警察类、土匪类3个类，警察类和土匪类继承公共类，功能函数都封装在父类公共类，特有的方法在子类中重写
#    3、db数据库接口层：sql_api.py  读取文件，将文件中的字典转换成字典格式，提供给后台逻辑函数使用
#    4、配置层：settings.py  定义数据库的连接信息（目前只用到文件，只是验证了数据库的登录操作，后续从文件过度到数据库使用）
#    5、文件中--表数据结构
#       1、用户表-username1.txt：用户名、角色名字、生命值、金币、武器、防弹衣等信息
# 	  2、武器明细表-shop_gun.txt：用户名、武器编号、武器名称、武器价格、购买数量等武器信息
# 	  3、加血操作历史记录表-addblood_his.txt：时间、登录IP、用户、角色、类型、增加生命值等操作信息
# 	  4、武器购买历史记录表-buygun_his.txt：时间、登录IP、用户、类型、消费金额等武器购买结算信息
# 	  5、武器伤害值表-weapons.txt:用户名、武器名、伤害值等武器攻击能力信息
# 2、功能描述
#    1、一共分为5个功能模块：1开战pk、2添加用户、3加血、4购买武器、5加血购买武器历史记录查询
#       这5个功能模块主要归结成3大类：1、管理接口：添加用户；2、对战模块：开战ok；3、对战辅助模块：加血、购买武器、加血购买武器历史记录日志查询
#    2、对战模块：开战ok--游戏的核心模块
#       1、采用回合制，先选择角色（警察或者土匪）
# 	  2、角色确定后，就发起攻击：
# 	     1、选择警察角色：
# 		    1、随机选择4种攻击武器中的一种，武器名和攻击力如下：B11-10 匕首-20 狙击枪-30 手雷-40
# 			   警察和土匪的初始血量（生命值）都是100，连续几轮攻击后，当土匪的血量小于0的时候，土匪就挂了
# 			   土匪受到B11手枪攻击，会掉血10；
# 			   土匪受到匕首攻击，会掉血20；
# 			   土匪受到狙击枪攻击，会掉血30；
# 			   土匪受到手雷攻击，会掉血40；
# 			2、土匪受到攻击后，掉血前，有2个功能判断：
# 			   1、1-3和1-2，2个随机数如果相等的话，土匪不掉血，躲过了攻击
# 			   2、判断土匪是否穿了防弹衣，如果穿了防弹衣，伤害会减半；土匪的防弹衣属性存在用户表中，默认土匪是没有防弹衣的
# 			      例如：土匪受到B11手枪攻击，如果没有防弹衣，会掉血10；如果有防弹衣，会掉血减半5
# 		 2、选择土匪角色：
# 		    1、随机选择4种攻击武器中的一种，武器名和攻击力如下：AK47-10 步枪-20 狙击枪-30 火箭筒-40
# 			   警察和土匪的初始血量（生命值）都是100，连续几轮攻击后，当警察的血量小于0的时候，警察就牺牲了
# 			   警察受到AK47攻击，会掉血10；（警察默认有防弹衣，掉血是5）
# 			   警察受到步枪攻击，会掉血20；（警察默认有防弹衣，掉血是10）
# 			   警察受到狙击枪攻击，会掉血30；（警察默认有防弹衣，掉血是15）
# 			   警察受到火箭筒攻击，会掉血40；（警察默认有防弹衣，掉血是20）
# 			2、警察受到攻击后，掉血前，有2个功能判断：
# 			   1、1-3和1-2，2个随机数如果相等的话，警察不掉血，躲过了攻击
# 			   2、判断警察是否穿了防弹衣，如果穿了防弹衣，伤害会减半；警察的防弹衣属性存在用户表中，默认警察是有防弹衣的，所以警察的掉血损伤会减半
# 			      例如：警察受到AK47攻击，如果没有防弹衣，会掉血10；如果有防弹衣，会掉血减半5
# 	  3、上述不管是警察还是土匪受到攻击的掉血，都是修改用户表中的生命值字段，减少生命值，通过公共类中的got_shot方法实现
# 	3、对战辅助模块：
# 	   1、加血：当警察和土匪快挂的时候，可以给警察或者土匪加血（增加生命值）
# 	      修改用户表中的生命值字段，增加生命值
# 	   2、购买武器：警察和土匪都可以买武器，增强攻击能力
# 	      购物武器明细表中：记录武器的名称，购买人和购买数量
# 		  修改用户表中的金币字段，减少金币值
# 		  修改武器明细表中的购买数量字段，增加购买数量
# 	   3、历史记录：
# 	      1、加血历史记录:
# 		     1、用户的每次加血记录都作为一个字典存在加血历史文件中，字典中记录加血时间、登录IP、用户、角色、类型、增加生命值等操作信息
# 			 2、前台打印加血历史记录的时候，通过json读取文件的加血字段，格式化打印加血历史记录
# 		  2、购买武器历史记录:
# 		     1、用户的每次购买记录都作为一个字典存在购买武器历史文件中，字典中记录武器购买时间、登录IP、用户、类型、消费金币等武器购买信息
# 			 2、前台打印武器购买历史记录的时候，通过json读取文件的相关字段，格式化打印购买武器历史记录
# 3、涉及的知识点
#    1、通过json(loads/dump)读写文件中的数据（文件中字典的形式组织存储数据）
#       1、json修改字典中字段
# 	  2、添加删除键值对
# 	  3、加血或者购买武器历史记录表：每一笔操作，都往历史记录文件中新增加一个字典，每个字典一行（dumps+手写换行符的方式，而不是dump的方式）
# 	      打印操作日志的时候，就一行一行像读取文件一样读取字典，json转换后变成字典处理，得到
# 		  时间、地点（登录IP）、人物（用户名）、事件（类型、交易金额）等日志要素
#    2、主函数、后台逻辑函数、数据接口、配置文件的模块导入功能和代码分层结构
#    3、socket得到ip地址：ipaddr = socket.gethostbyname(socket.gethostname())
#    4、主函数结构的优化：主函数main中分支流程判断用字典实现，来逐步代替if--else分支太多的情况
#       每个分之值调用一个方法的时候，用字典来实现，很简洁；
# 	  对于分之中需要连续调用多个方法的时候，暂时还用if-else分之来写
#    5、通过随机数和字典，随机选取武器发动进攻
#    6、面向对象的思想
#       1、类的继承、实例、通过实例调用方法
# 	  2、方法封装到父类中，子类的实例可以直接调用
# 	  3、子类对父类方法的重写
# 	  4、子类对父类初始化方法中属性的重写和继承
# 	  5、子类特有的方法，只能子类的实例才能调用，别的类的实例是无法调用的
# 	     例如：警察类的特有方法，解救人质方法，只能警察类的警察实例才能调用，土匪类的土匪实例就无法调用
# 	  6、实例中的实参，传到初始化方法后，可以直接用self.形参在类中的多个方法中引用
# 	     例如：购买武器方法中的形参只有gun_name(武器名字)，如果想打印是谁买的武器，可以直接用self.name这个参数代替
# 4、后续需要优化的地方
# 	1、所有涉及生命值减少或者增加的操作，都统一由一个方法实现，其余方法用到生命值增加或者减少，直接调用即可
# 	2、所有涉及金币增加或者减少的操作，都统一由一个方法实现，其余方法用到金币增加或者减少，直接调用即可
# 	3、目前设计的游戏pk是回合制的，还没有实现双方互打的情况
# 	4、目前功能还比较少，后续可以扩展下述功能：
# 	    1、警察每解救一个人质，金币奖励1000
# 	    2、土匪每杀死一个人质，警察金币减少800
# 		3、土匪每次投降，警察金币奖励1500
