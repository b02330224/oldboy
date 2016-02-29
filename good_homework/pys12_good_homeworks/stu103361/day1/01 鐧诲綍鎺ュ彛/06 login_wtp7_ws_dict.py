__author__ = 'Administrator'
# -*- coding:utf-8 -*-

# user_map = {
#     "jack":{"pwd": "123", "times": 0},
#     "tom":{"pwd": "123", "times": 0}
# }

#将文件中的内容读入内存
obj = open("db","r+")  #读写模式打开文件对象

#构造成字典模式(将文件中的字符串先转换成列表，再通过列表来构造字典)
user_map = {}  #定义空字典
for i in obj: #遍历文件对象，得到每一行作为元素存入列表
    # print i.strip().split(";")  #['tom', '123', '0']
    user_info_list = i.strip().split(";")  #去掉换行后，用;作为分隔符，拆分成列表
    user_map[user_info_list[0]] = {"pwd": user_info_list[1], "times": int(user_info_list[2])}
    #通过列表的索引号构造成字典，times登录次数转换成了int
    # print user_map #{'jack': {'pwd': '123', 'times': '0'}, 'tom': {'pwd': '123', 'times': '0'}}

while True:  #定义一个外循环，用户名为空或者不存在的情况，会重复要求输入
    # flag = 0 #定义flag，用于判断输入的用户是否存在，存在将flag置为1，不存在flag==0，代表用户不存在
    username = raw_input("请输入用户名:") #要求用户输入用户名
    if len(username)==0:  #如果用户输入的用户名是空
        print "\033[31;1m用户名不能为空\033[0m"
        continue    #跳出本次循环（本次迭代），进行下一次循环
    elif username not in user_map: #如果用户输入的用户名不正确， 这里是not in
        print "\033[31;1m用户名不存在，请重新输入!\033[0m"  #红色字体提示失败
    else:  #如果用户输入的用户名正确， 这里是in
        while True:   #定义一个内循序，用于要求用户输入密码，密码不对的情况，会重复要求输入，直到输入正确或者break
            passwd = raw_input("请输入密码:")#要求用户输入密码
            # passwd = getpass.getpass("请输入密码:")  #getpass不显示密码密文
            if passwd == user_map[username]["pwd"] and user_map[username]["times"] <3: #用户输入的密码和字典的（密码字段）对比，且字典的（登录错误次数）<3
                user_map[username]["times"] = 0 # 字典（登录错误次数）置为0
                print "\033[32;1m登录成功，欢迎 %s\033[0m" % username  #绿色字体提示成功
                break  #跳出内循环while（不会要求再次输入密码）
            elif user_map[username]["times"] >=3: #字典（登录错误次数）>=3
                print "\033[31;1m登录账号锁定，请联系管理员!\033[0m" #红色字体提示锁定失败
                break  #跳出内循环while（不会要求再次输入密码）
            else:  #用户名正确，密码不对且登录错误次数<3
                user_map[username]["times"]+= 1 #字典（登录错误次数）自增1
                times_left = 3-user_map[username]["times"]  #定义还有几次尝试机会（剩余尝试机会+登录错误次数=3）
                if times_left ==0: #剩余尝试机会为0
                    print "\033[31;1m登录账号锁定，请联系管理员!\033[0m" #红色字体提示锁定失败
                    break #跳出内循环while（不会要求再次输入密码）
                else:#剩余尝试机会不是0（2次，1次）
                    print "\033[31;1m密码输入错误，请重新输入,您还有 %s 次输入机会\033[0m"% times_left #红色字体提示失败
                    continue
        temp_list = []  #定义空列表
        for key, value in user_map.items(): #遍历字典的key和value items必须的有
            temp = "%s;%s;%d" % (key, value['pwd'], value['times']) #拼接字符串 tom;123;0
            # print temp  #tom;123;0
            temp_list.append(temp)   #将字符串作为元素添加到空列表 ['jack;123;3', 'tom;123;0']
        # print temp_list
        temp_str = "\n".join(temp_list)  #以换行符\n作为连接符 join2个元素，变成一个大字符串，分成2行
        # print temp_str  #"jack;123;0\ntom;123;0"
        # w_obj = open('db', 'w') #前面13行如果是只读r模式，这里就可以写模式再创建一个文件
        obj.seek(0)  #前面13行是读写r+模式，回到文件的最开始处
        obj.write(temp_str)  #将修改完登录次数的字符串写入文件
        obj.flush()  #刷新缓存
        obj.close()  #关闭文件对象
        break  #写完文件后，退出外循环



