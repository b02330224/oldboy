__author__ = 'Administrator'
# -*- coding:utf-8 -*-

#只读取文件，计算余额这块，不打印购物清单，主要为了验证余额计算逻辑是否正确

total = 0  #商品总价格的初始值
num =10000  #定义用户的预算（兜里一共10000元）
break_flag = False  #跳出外循环标识

while True:  #定义一个外循环，商品编号为空27行或者不存在87行的情况，会一直重复要求输入
    old_list = []  #定义空列表1，用于将文件中读取的字符串去换行符strip,split拆分成字符串作为元素存到列表
    new_list = [] #定义空列表2，用于将修改了购买数量的列表，join成字符串添加到空列表中，最终写入文件
    flag = 0 #定义flag，用于判断输入的商品编号是否存在，存在将flag置为1，不存在flag==0，代表商品编号不存在

    #读文件
    f = open("shopping.txt","r") #只读模式读取文件到内存
    for i in f:  #遍历文件
        line_list =  i.strip().split("|")  #['1', 'iphone6s', '7000', '0'] 将字符串去换行符,拆分成列表
        try:
            line_list[-1] = int(line_list[-1])  #将购买数量、商品价格转换成int，方便计算（购买数量+1）
            line_list[-2] = int(line_list[-2])
        except Exception,e:
            line_list[-1] =0  #处理异常，如果购买数量、商品价格无法转换成int，说明不是数字字符，就置为购买数量是0，商品价格是7777
            line_list[-2] =7777
        old_list.append(line_list)  #将2个子列表添加到空列表1中
        # print old_list #[['1', 'iphone6s', 7000, 0], ['2', 'mac', 8888, 0]]

    goods_no_input = raw_input("请输入商品编号:") #要求用户输入商品编号
    if len(goods_no_input)==0:  #如果用户输入的商品编号是空
        print "\033[31;1m商品编号不能为空\033[0m"
        continue    #跳出本次循环（本次迭代），进行下一次循环（要求重复输入）

    for j in old_list:  #遍历列表，得到2个子列表
        # print j   #['1', 'iphone6s', 7000, 0]
        if goods_no_input == j[0]:   #如果用户输入的商品编号正确，j[0]代表文件中商品编号字段
            flag = 1  #商品编号标识变成1 （下面5行，要是构造字典的话，可以这么写，但是列表遍历就不行了）
            # if len(goods_no_input)==0: #如果商品编号为空
            #     print "\033[31;1m商品编号不能为空\033[0m"
            # elif goods_no_input not in shop_dict: #如果商品编号不存在
            #     print "\033[31;1m商品编号不存在\033[0m"
            # else: #商品编号存在
            # 商品总价格和购买数量变动运算
            if  total < num: #bug修复，当商品总价格超过用户预算的时候，就不要再累加商品价格了，否则会出现61行，余额是负数的情况
                # total += shop_dict[goods_no_input]["price"]  #累加商品的价格（需要支付多少钱）--字典
                total += int(j[-2]) #累加商品的价格（需要支付多少钱）--列表
                # print total
    # # 先计算商品总价格，再将商品总价格和预算比对
            if total < num: #如果需要支付的钱小于用户的预算
                 # shop_dict[goods_no_input]["times"] += 1  #购买数量+1--字典
                 j[-1] +=1 #购买数量+1--列表
                 left_money = num - total   #用户预算扣除购物车的总花费后，计算用户的余额
                 print "\033[32;1m没有超出预算，还剩余%s元余额,可以继续购买\033[0m" % left_money
                 break #跳出for遍历循环（内循环），回到while外循环，重新输入商品编号
            if total >= num: #如果需要支付的钱大于等于用户的预算，钱不够了，计算用户余额和用户买这个商品还差多少钱
                cha_money = total - num #商品总价格-用户预算=用户差的钱
                # left_money = shop_dict[goods_no_input]["price"]-cha_money   #余额--字典
                left_money = j[-2]-cha_money  #余额--列表     #（用户差的钱+用户的余额=商品的价格）
                print "\033[31;1m钱不够了,还剩余%s元余额，想要买这件商品，还差%s元\033[0m" % (left_money,cha_money)
                while True:#定义内循环，判断退出
                    tuichu = raw_input("确认退出程序么？输入q，退出程序；输入b，返回上一级菜单:")
                    if tuichu == "q":  #
                        print "\033[32;1m退出程序,打印购物单如下：\033[0m"
                        break_flag = True  #外循环退出标识
                        break  #跳出内循环while
                    elif tuichu == "b":
                        # total -= shop_dict[goods_no_input]["price"] #返回上一级的时候，最后一个商品由于预算不够，所以必须要扣减最后一个商品的价格--字典
                        total -= j[-2] #bug修复，返回上一级的时候，最后一个商品由于预算不够，所以必须要扣减最后一个商品的价格--列表
                        print "\033[32;1m返回上一级菜单,请重新输入你要买的商品编号:\033[0m"
                        break #跳出内循环while，回到外循环while（重新输入商品编号）
                    else:  #如果输入的不是q或者b
                        print "\033[31;1m您输入的指令无效，请重新输入\033[0m"
                        continue  #跳出内循环本次迭代，继续输入指令

        if goods_no_input == j[0]:#由于31行是遍历列表，如果输入的商品编号是1，那么只有1的购买数量加1,2的就不能加1
            j[-1]+=1  #购买数量+1
        j[-1] = str(j[-1])#列表最后1项（购买数量）转换成字符串类型，方便写入到文件  缩进必须在if goods_no_input == j[0]同级
        j[-2] = str(j[-2])#列表倒数第2项（商品价格）转换成字符串类型，方便写入到文件
        new_list.append("|".join(j)) #将列表的元素用|连接join成字符串，作为元素添加到新空列表2中（修改购买数量后，写入到文件）
        # print new_list  #['1|iphone6s|7000|0', '2|mac|8888|1']
    if flag == 0: #用户标识是1代表商品编号存在34行，商品标识是0代表商品编号不存在（用户输入的商品编号，文件中没有）
        print "\033[31;1m商品编号不存在，请重新输入!\033[0m"  #红色字体提示失败
        continue
    if break_flag: #61行，用户输入q后，外循环条件具备
        break  #跳出外循环while，不在要求输入商品编号
#4最后将购买数量修改后，从列表-内存写入到新的文件
new_str = "\n".join(new_list) #用\n换行符作为连接符，连接2个字符串，形成一个2行的字符串
f = open("shopping1.txt","w")  #写的模式，新创建一个文件对象
f.write(new_str) #将换行后的2行字符串写入到文件
f.close() #关闭文件对象




