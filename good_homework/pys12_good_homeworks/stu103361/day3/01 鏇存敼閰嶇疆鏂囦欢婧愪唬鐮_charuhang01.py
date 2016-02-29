__author__ = 'Administrator'
#-*- coding:utf-8 -*-
import re

#1处理用户输入的字典,将字典的key处理成已经排序的列表，用于拼接字符串
def chushihua(arg1):  #arg1是形式参数  主模块mydic是实际参数传入（调用函数的时候，传入实参）
    li_dickey=arg1.keys()   #将用户输入的字典的key添加到列表，无序的，无法通过索引号定位
    li_dickey = list(li_dickey)  #字典的key需要转换成list，才能排序
    li_dickey.sort()   #将列表排序后，通过索引号取出字典的key
    return li_dickey   #返回已经排序的列表

#2计算要插入的字符串的索引号  3
#2也可以实现根据用户的输入，查找匹配的标题行，并且显示标题行下面的内容--查询功能
def cal_index(arg2):  #arg2是形式参数  主模块mydic是实际参数传入（调用函数的时候，传入实参）
    ret = chushihua(arg2)  #调用列表排序函数1
    mystr = "%s %s" % (ret[0],arg2[ret[0]])  #拼接要查找的目标行的标题行
    f = open("ha_proxy.txt","r")   #只读模式打开配置文件对象
    li = [] #定义空列表
    flag = False #定义标识
    for i in f: #遍历文件
        # i = i.replace("\t\t","\t")
        i = re.sub("\t+","\t",i) #这个正则可以将多个tab键\t转换成1个tab键
        i = i.expandtabs()
        if i.strip() == mystr:   #找哪一行去掉换行符后，是==backend buy.oldboy.org 用了变量
            flag = True   #将标识符置为True（这个是后面2个if执行的前提）
            # li.append(i.strip())  #'backend test.oldboy.org'
            continue    #当次迭代停止（下面的代码不执行），进入下一次迭代
        if flag and i.strip().startswith("backend"): #当标识符是True且当前行的开头是“buy.oldboy.org” 用了形参
            break    #跳出整个for循环，不需要再取了（目标是将配置文件ha_proxy的第29,30行取出，存入列表）
        if flag and  i.strip():  #标识符是True且当前不是空白（如果当前行空白，i.strip()是false）
            li.append(i.strip())   #把找到的行添加到空白列表 #['backend test.oldboy.org', 'server 100.1.7.9 100.1.7.9 weight 20 maxconn 3000', 'server 100.1.7.999 100.1.7.999 weight 20 maxconn 3000']
    # print(len(li))  #34  27
    # print(li) #['backend test.oldboy.org', 'server 100.1.7.9 100.1.7.9 weight 20 maxconn 3000', 'server 100.1.7.999 100.1.7.999 weight 20 maxconn 3000']
    for i in li:
        print(i)
    return(len(li))  #3
    f.close()
# cal_index(mydic)


#3插入目标行到列表
def zhuanhuan(arg3):
    #1拼接字符串，用于确定目标插入行的索引号
    ret = chushihua(arg3)  #调用列表排序函数1
    mystr = "%s %s" % (ret[0],arg3[ret[0]])  #ret[0]不能加双引号
    # print(mystr)  #backend test.oldboy.org

    #2 查找索引号
    f = open("ha_proxy2.txt","r")   #只读模式打开文件对象
    li = [] #定义空列表
    for i in f: #遍历文件
        # i = i.replace("\t\t","\t")  #将2个tab键变成1个tab键，对齐
        i = re.sub("\t+","\t",i) #这个正则可以将多个tab键\t转换成1个tab键
        i = i.expandtabs()
        line = i.rstrip()  #去掉每行右边的换行符
        li.append(line)
    # print(li) #文件的每行作为一个元素存在列表li中
    index_num = li.index(mystr) #查找索引号
    # print(li.index(mystr))  #27
    f.close()

    #3拼接待插入的字符串
    dic2 = arg3[ret[1]]   #处理入参
    ret2 = chushihua(dic2)  #调用列表排序函数1
    # print(dic2)  #{'server': '100.1.7.999', 'maxconn': 30, 'weight': 20}
    # print(ret2)  #['maxconn', 'server', 'weight']
    write_str = "\t%s %s %s %s %s %s %s" % (ret2[1],arg3[ret[1]][ret2[1]],arg3[ret[1]][ret2[1]],ret2[2],arg3[ret[1]][ret2[2]],ret2[0],arg3[ret[1]][ret2[0]])
    write_str = write_str.expandtabs()  #用于将\t转换成8个空格，统一对齐
    # print(write_str)  #server 100.1.7.999 100.1.7.999 weight 20 maxconn 30

    #4 插入到列表指定位置
    result = cal_index(arg3) #调用函数2，返回3
    li.insert(index_num+result+1,write_str)
    # print(li) #在backend test.oldboy.org 对应的索引号27，后面的索引号是30行处，插入待插入字符串
    f.close()
    return li  #返回值是修改后的列表（已经插入了目标行）


# 5 写入到文件（不管是添加行还是删除行，对列表修改后，都需要重新写入到文件）
def writenew(arg4):  ##arg4是形式参数  li是实际参数传入（调用函数的时候，传入实参,第一个函数的返回时li）
    mystr_new = "\n".join(arg4)  #换行符作为连接符，连接列表的每个元素（每个元素一行）
    print("修改后的配置文件如下：\n",mystr_new)  #打印修改后的配置文件(添加或者删除)
    f = open("ha_proxy2.txt","w") #新建一个文件，用于存放修改后的ha_proxy文件
    f.write(mystr_new) #写入到新文件
    f.close() #关闭文件对象

# ret = zhuanhuan()
# writenew(ret)

#6删除目标行到列表
def zhuanhuan2(arg3):
    #1拼接字符串，用于确定目标删除行的索引号
    ret = chushihua(arg3)  #调用列表排序函数1
    mystr = "%s %s" % (ret[0],arg3[ret[0]])  #ret[0]不能加双引号
    # print(mystr)  #backend test.oldboy.org

    #2 查找索引号
    f = open("ha_proxy3_del.txt","r")   #只读模式打开文件对象
    li = [] #定义空列表
    for i in f: #遍历文件
        # i = i.replace("\t\t","\t")  #将2个tab键变成1个tab键，对齐
        i = re.sub("\t+","\t",i) #这个正则可以将多个tab键\t转换成1个tab键
        i = i.expandtabs()
        line = i.rstrip()  #去掉每行右边的换行符
        li.append(line)
    # print(li) #文件的每行作为一个元素存在列表li中
    index_num = li.index(mystr) #查找索引号
    # print(li.index(mystr))  #27
    f.close()

    #3拼接待删除的字符串
    dic2 = arg3[ret[1]]   #处理入参
    ret2 = chushihua(dic2)  #调用列表排序函数1
    # print(dic2)  #{'server': '100.1.7.999', 'maxconn': 30, 'weight': 20}
    # print(ret2)  #['maxconn', 'server', 'weight']
    write_str = "\t%s %s %s %s %s %s %s" % (ret2[1],arg3[ret[1]][ret2[1]],arg3[ret[1]][ret2[1]],ret2[2],arg3[ret[1]][ret2[2]],ret2[0],arg3[ret[1]][ret2[0]])
    write_str = write_str.expandtabs()  #用于将\t转换成8个空格，统一对齐
    # print(write_str)  #server 100.1.7.999 100.1.7.999 weight 20 maxconn 30

    #4 从列表指定位置删除
    result = cal_index(arg3) #调用函数2，返回3
    li.pop(index_num+result+1)  #从字典删除指定索引号的元素
    # print(li) #在backend test.oldboy.org 对应的索引号27，后面的索引号是30行处，插入待插入字符串
    f.close()
    return li  #返回值是修改后的列表（已经删除了目标行）


