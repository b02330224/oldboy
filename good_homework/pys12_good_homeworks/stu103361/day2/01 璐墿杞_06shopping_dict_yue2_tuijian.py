__author__ = 'Administrator'
# -*- coding:utf-8 -*-

# 打印购物列表
# 死循环
# 预算多少钱
# 1、iphone6s 6099
# 2、mac      8888
#
# 输入要买的:1
# 一把iphone加入购物车，还剩多少钱?
# 最后退出：
# 打印已购商品，同时结余

#整体思路：
# 逻辑分支
# 1 商品编码为空
# 2 商品编码不存在
# 3 商品编码存在
#   a 待支付的钱小于用户预算，可以继续购买
#   b 待支付的钱大于等于用户预算，提示余额和还差多少钱
#     1按q退出整个程序，打印购物清单，显示余额
#     2按b返回上一级菜单，要求用户输入商品编号
#     3按其他指令，提示指令无效，重新输入

# 步骤：
# 1读文件到内存，构建字典
# 2修改内存中字典的购物数量
# 3将修改后的购物数量写入到新的文件
# 4打印购物清单

# 购物车余额单独存文件、数据库、json、pickle--钱在第一次退出后，下次再进来还能看到余额-
# 1、余额存在单独文件中，读出来存在列表
# 2、列表中修改余额
# 3、将修改后的余额写入文件

# 涉及的知识点
# 1提示语颜色
# 2异常处理-如果购买数量或者价格不是数字，就把购买数量置为数字0，价格置为数字7777
# 3打印购物清单，对齐显示购物清单，左对齐
#   print ('%-11s%-11s%-11s%-11s' % (l_list[0], l_list[1],l_list[2], l_list[3]))
# 4显示余额和差额数学计算
# 5 字典构建
#   shop_dict[line_list[0]] = {"goods":line_list[1],"price":int(line_list[-2]),"times":int(line_list[-1])}

# 踩过的坑：84行 106行  (debug print)--3hour
# 84行 当商品总价格超过用户预算的时候，就不要再累加商品价格了，否则会出现98行，余额是负数的情况
# 106行 返回上一级的时候，最后一个商品由于预算不够，所以必须要扣减最后一个商品的价格

#退出后显示余额，踩过的坑：
# 1、余额先从str转换成int后，必须从int转换成str，否则181行报错 my_str = "|".join(yue_list)
# 2、原始的余额是10000，存在文件中，每买一件商品，余额必须扣减商品的价格  yue_list[-1] -= total
     #否则，余额无法改变（购买数量+=1;余额-=商品价格；错误登录次数+=1）

# shop_dict = {
#     "1":{"goods":"iphone6s","price":"6099"}
#     "2":{"goods":"mac","price":"8888"}
# }

#1读文件,构造字典
f = open("shopping.txt","r")  #只读模式打开文件对象
shop_dict = {}  #定义空字典
for i in f:  #遍历文件
    line_list = i.strip().split("|")  #字符串去掉换行，以"|"为分隔符拆分成列表
    try: #异常处理，如果购买数量或者价格不是数字，就把购买数量置为数字0，价格置为数字7777
        line_list[-2] = int(line_list[-2])
        line_list[-1] = int(line_list[-1])
    except Exception,e:
        line_list[-2] = 7777
        line_list[-1] = 0
    shop_dict[line_list[0]] = {"goods":line_list[1],"price":int(line_list[-2]),"times":int(line_list[-1])}
    #商品价格和购买数量转换成int，便于计算
    # print shop_dict # {'1': {'price': 6099, 'goods': 'iphone6s', 'times': 0}, '2': {'price': 8888, 'goods': 'mac', 'times': 0}}

# 2读文件中的余额，不用构造字典，列表的索引即可以表示yue_list[-1]
f1 = open("shopping_yue.txt","r")  #读出预算(第二个字段)或者余额（最后一个字段），余额变动后，再次写入到文件
# yue_dict = {}
for j in f1:  #遍历文件
    yue_list = j.strip().split("|")  #字符串去掉换行，以"|"为分隔符拆分成列表
    print yue_list
    try: #异常处理，如果购买数量或者价格不是数字，就把购买数量置为数字0，价格置为数字7777
        yue_list[-2] = int(yue_list[-2])
        yue_list[-1] = int(yue_list[-1])
    except Exception,e:
        yue_list[-2] = 10000
        yue_list[-1] = 10000
    # yue_dict[yue_list[0]] = {"yusuan":int(yue_list[-2]),"yue":int(yue_list[-1])}
    # print yue_dict  #{'jack': {'yusuan': 10000, 'yue': 10000}}

#3修改购物数量（内存字典中）
total =0 #定义商品一共多少钱
num = 10000  #定义购物预算（兜里一共多少钱） 预算可以直接定义，也可以从文件中读取yue_list[-2]
# num = int(yue_list[-2])
# left_money =int(yue_list[-1])
break_flag = False  #跳出外循环标识
my_list = []


while True: #外循环，输入商品编号
    print "---商品编号列表---"
    print ('%-15s%-15s%-15s%-15s' % ("商品编号", "商品名称","商品价格", "购买数量"))
    f = open("shopping.txt","r")
    for i in f:
        line_list = i.strip().split("|")
        print ('%-11s%-11s%-11s%-11s' % (line_list[0], line_list[1],line_list[2], line_list[3]))
    #打印商品编号列表
    print "您的余额目前是%s元" % yue_list[-1]
    goods_no_input = raw_input("请输入你要买的商品编号:") #要求用户输入商品编号
    if len(goods_no_input)==0: #如果商品编号为空
        print "\033[31;1m商品编号不能为空\033[0m"
    elif goods_no_input not in shop_dict: #如果商品编号不存在
        print "\033[31;1m商品编号不存在\033[0m"
    else: #商品编号存在
        if  total < num: #bug修复，当商品总价格超过用户预算的时候，就不要再累加商品价格了，否则会出现98行，余额是负数的情况
            total += shop_dict[goods_no_input]["price"]  #累加商品的价格（需要支付多少钱）
            # print total
        # # 先计算商品总价格，在将商品这价格和预算比对
        if total < num: #如果需要支付的钱小于用户的预算
            shop_dict[goods_no_input]["times"] += 1  #购买数量+1
            # print yue_list[-1]
            yue_list[-1] -= total    #关键点：原始的余额是10000文件中，每买一件商品，余额扣减商品的价格
            # print yue_list[-1]
            # yue_list[-1] = num - total   #用户预算扣除购物车的花费后，计算用户的余额
            print "\033[32;1m没有超出预算，还剩余%s元,可以继续购买,输入c，退出程序；输入a，继续购买:\033[0m:" % yue_list[-1]
            while True:
                tuichu1 = raw_input("确认退出程序么？输入c，退出程序；输入a，继续购买:")
                if tuichu1 == "a":
                    break  #跳出循环的当前迭代，回到75行
                elif tuichu1 == "c":
                    break_flag = True  #外循环跳出标签
                    break
                else:  #如果输入的不是a或者c
                    print "\033[31;1m您输入的指令无效，请重新输入\033[0m"
                    continue  #跳出内循环本次迭代
                    # print total
            if break_flag:
                break  #跳出外循环
        if total >= num: #如果需要支付的钱大于等于用户的预算，钱不够了，计算用户余额和用户买这个商品还差多少钱
            cha_money = total - num #商品总价格-用户预算=用户差的钱
            # yue_list[-1] = shop_dict[goods_no_input]["price"]-cha_money
        #如果left_money为负数，取绝对值（用户差的钱+用户的余额=商品的价格）
            print "\033[31;1m钱不够了,还剩余%s元，想要买这件商品，还差%s元\033[0m" % (yue_list[-1],cha_money)
            while True:#定义内循环，判断退出
                tuichu = raw_input("确认退出程序么？输入q，退出程序；输入b，返回上一级菜单:")
                if tuichu == "q":  #
                    print "\033[32;1m退出程序,打印购物单如下：\033[0m"
                    break_flag = True  #外循环退出标识
                    break  #跳出外循环
                elif tuichu == "b":
                    total -= shop_dict[goods_no_input]["price"]
                    #bug修复，返回上一级的时候，最后一个商品由于预算不够，所以必须要扣减最后一个商品的价格
                    # print total
                    print "\033[32;1m返回上一级菜单,请重新输入你要买的商品编号:\033[0m"
                    break #跳出内循环本次迭代
                    # continue
                else:  #如果输入的不是q或者b
                    print "\033[31;1m您输入的指令无效，请重新输入\033[0m"
                    continue  #跳出内循环本次迭代
            if break_flag:
                break  #跳出外循环

#4将修改后的购物数量写入到新的文件，字典拼接字符串
temp_list= []  #定义空列表
for k,v in shop_dict.items():  #遍历字典的项目items()  key value（k v）--items（）必须
    mystr = "%s|%s|%s|%s" % (k,v["goods"],str(v["price"]),str(v["times"]))
    #用k v模式拼接字符串 (将购买数量和商品价格转换成字符串，用于写入)
    print mystr
    temp_list.append(mystr)  #将字符串作为元素添加到空列表
    # print temp_list
# f.seek(0)  #回到文件最开始
temp_str = "\n".join(temp_list)  #将列表的2个元素用换行符分隔，转换成字符串
f = open('db2', 'w')  #写的模式，新创建一个文件
f.write(temp_str) #写入字符串
f.flush()  #关闭文件前，最好带上（刷新缓存）
f.close() #关闭文件对象（句柄）

#5将修改后的余额写入到新的文件
yue_list[-1] =  str(yue_list[-1])   #余额必须从int转换成str，否则181行报错
yue_list[-2] =  str(yue_list[-2])   #预算必须从int转换成str
# print type(yue_list[-1])
# print yue_list
my_str = "|".join(yue_list) #以连接符"|"连接列表的元素，组成一个字符串
# print my_str
my_list.append(my_str)
    # print my_list #['jack|123|1', 'tom|123|1']
# print f.tell()
# f.seek(0)  #回到文件最开始
my_str = "\n".join(my_list)  #tom|123|1
f = open('db4', 'w')  #写的模式，新创建一个文件
f.write(my_str) #将1行字符串写入文件
f.close() #关闭文件对象（句柄）

#6打印购物清单
f = open ('db2', 'r')   #读取修改购买数量后的文件到内存
print "----购物清单----"
print ('%-15s%-15s%-15s%-15s' % ("商品编号", "商品名称","商品价格", "购买数量"))
#‘%-15s’表示在字符串后面添加占位符，字符串采用左对齐的方式。
for i in f:   #遍历文件
    l_list = i.strip().split("|")   #去换行后，以"|"作为分隔符拆分成列表
    print ('%-11s%-11s%-11s%-11s' % (l_list[0], l_list[1],l_list[2], l_list[3]))
    #单独采用‘%s’时，直接输出字符串，
    # ‘%10s’表示在字符串前面添加占位符，并且字符串采用右对齐的方式，
    # ‘%-10s’表示在字符串后面添加占位符(这10位占位符包含字符串)，字符串采用左对齐的方式。
    #   例如字符串本身是"abc"3位，那么‘%-10s’表示在字符串"abc"后添加7位占位符
print "结算后，您的余额是:%s元" % yue_list[-1]
f.close() #关闭文件

# ----购物清单----
# 商品编号   商品名称   商品价格   购买数量
# 1          iphone6s   6099       1
# 2          mac        8888       0

# a ="123"
# b = "234"
# print('%-4s%-10s' % (a, b))















