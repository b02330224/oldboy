__author__ = 'Administrator'
#-*- coding:utf-8 -*-

# import sys
# print(sys.path)


#功能实现：实现配置文件的插入行、查询、删除行、修改行功能
# 代码结构说明：
# 一共2个文件 文件index00.py是主模块
# 文件charuhang01.py是功能模块，功能模块包含2个def函数，
# def1：函数zhuanhuan用于
#  1、根据输入的字典，拼接字符串，用于确定应该在列表（读取文件的每行到列表）的哪个位置插入（依据索引号）；
#  2、拼接要插入字符串，插入到列表指定位置
# def2：函数writenew用于
#  1、将修改后的列表（插入了一行的）重新写入到文件（这里新建了一个新文件，主要用于测试，也可以在原文件读写）


# 整体思路：
# 主函数main输入的字典存在变量 该变量作为调函数的实际参数 主函数全是函数调用def1 def2
# def1  将输入转换成字典 得到要插入行的索引号  参数是输入变量 不用return
# def2 拼接要插入的字符串 插入到列表指定位置
# def3 将修改后的列表写入新文件
# 参数是列表 不用return
# 2输入字符串转换成json load  输入的是列表，字典 这些都是字符串 通过json load就是字典，列表---def1
# 3遍历文件 得到要插入行的索引号 传入实际参数
# 4将修改后的列表写入文件…def2
# 5主函数输入 转换成字典加异常处理 转换失败 要求重新输入
#
# 逻辑主流程都放在main 功能都封装到def
# def1 往列表插入一行
# def2 将修改后列表写入新文件
#
# def1找插入位置 索引号
# def2通过字典拼接待插入的字符串到列表
# def3将修改后列表写入新文件
#
# def1输入字符串类型的字典转换成字典
# def2读文件 找插入位置
# def3拼接字符串
# def4重新写入
#
# 一共2个文件 文件1主函数 文件2…def1 def2 def3  上述3个写法

#踩过的坑：
#1、把输入的字符串转换成字典 ，应该用loads而不是load
#2、字典的key需要转换成list，才能排序
#3、ret[0]不能加双引号，因为已经是字符串了
#4、文件的编码格式默认是ascii，改成unicode会出现乱码或者GBK错误

#用户输入的字典(查询和插入行用户都是输入的这个字符串)
#{"backend": "test.oldboy.org","record":{"server": "100.1.7.999","weight": 20,"maxconn": 30}}

# 涉及的知识点：
# 1 json的loads：用于将用户输入的字符串类型的字典转换成字典操作；
# 2 异常处理：如果字典中含有中文标点，json转换会报错，异常处理后，要求用户重新输入
# 3 字符串格式化
# 4 函数式编程（一共2个文件 文件1主函数 文件2…def1 def2 def3 def4功能函数 ）
#   主函数文件：调用 def3--往列表添加目标行；
#             调用 def4--将修改后的列表写入到新的文件（def3的返回值，作为def4的参数）
#   功能函数文件：def1 1处理用户输入的字典,将字典的key处理成已经排序的列表，用于拼接字符串
#    def2 2计算要插入的字符串的索引号(标题行下面的非空行有几行)
#    def3 3插入目标行到列表
#         1 调用列表排序函数-def1
#         2 拼接字符串，读取文件到列表，用于确定标题行back在列表中的索引号
#         3 调用列表排序函数-def1，拼接待插入的字符串（三层字典）
#         4 调用函数2，返回back标题行下面有2个非空行，插入到列表指定位置（back索引号 +3）
#    def4 4将修改后的列表写入到文件
#  5 文件读写
#  6 字典的key存在列表中，排序，通过索引号取出字典的key
#  7 拼接待插入的字符串，需要格式化三层字典，通过索引号取出字典的第一层key以及嵌套字典的key
#  8 函数式编程中 参数传递，返回值return
#     参数传递：主函数文件中的字典mydic作为实际参数，传入到功能函数文件def1 def2 def3
#                   这3个参数的形式参数可以不是mydic,可以改成arg1 arg2 arg3
#                    函数调用的时候，传入的是实际参数mydic;定义函数的时候，参数是形参；调用函数的时候，是实参
#             功能函数文件中的def3返回的修改后的列表li,作为def4文件写入函数的参数
#     函数调用：主函数调用def3 def4
#              def2调用1次def1-列表排序  def3调用2次def1-列表排序（分别用于标题行字符串拼接和带插入字符串拼接）
#     返回值：def1 def2 def3都有返回值return  def4没有返回值（文件读写）
#  9 正则表达式，将多个tab键\t转换成1个\t  i = re.sub("\t+","\t",i) #这个正则可以将多个tab键\t转换成1个tab键
#  10 用expandtab将制表符-tab键\t 统一转换成8个空格（避免有的tab是4个空格，有的是8个空格的情况）

import charuhang01  #导入功能模块
import json


if __name__ == "__main__":
    print("请选择配置文件操作类型")
    print("%s%s%s%s%s"%("1、添加行\n","2、删除行\n","3、修改行\n","4、查看行\n","5、退出系统"))
    while True:
        choice = input("请输入操作序号:")
        if choice == "1":  #往配置文件指定地方插入一行
            myinput = input("请输入需要添加到配置文件的内容：") #输入的是字符串类型的字典
            try:
                mydic = json.loads(myinput)  #把输入的字符串转换成字典  注意方法是loads而不是load
            except Exception: #异常处理，如果输入的字典格式不对，例如中文标点之类，要求用户重新输入
                myinput = input("\033[31;1m字典输入格式不正确，请重新输入需要添加的内容：\033[31;1m")
            ret = charuhang01.zhuanhuan(mydic)  #往列表添加目标行.mydic是实际参数
            charuhang01.writenew(ret)   #将修改后的列表写入到新的文件
            #函数2-writenew将函数1-zhuanhuan的返回值，作为参数传入
            print("\033[32;1m配置文件添加行成功\033[31;1m")
            break
        elif choice == "2": #往配置文件指定地方删除一行
            # print("\033[33;1m删除功能还未提供，敬请期待\033[0m")
            myinput = input("请输入需要删除的配置文件的内容：") #输入的是字符串类型的字典
            try:
                mydic = json.loads(myinput)  #把输入的字符串转换成字典  注意方法是loads而不是load
            except Exception: #异常处理，如果输入的字典格式不对，例如中文标点之类，要求用户重新输入
                myinput = input("\033[31;1m字典输入格式不正确，请重新输入需要删除的内容：\033[31;1m")
            ret = charuhang01.zhuanhuan2(mydic)  #往列表添加目标行.mydic是实际参数
            charuhang01.writenew(ret)   #将修改后的列表写入到新的文件
            #函数2-writenew将函数1-zhuanhuan的返回值，作为参数传入
            print("\033[32;1m配置文件删除行成功\033[31;1m")
            break
        elif choice == "3": #修改的逻辑是，先删除指定行，然后添加新的内容到指定行
            # print("\033[34;1m修改功能还未提供，敬请期待\033[0m")
            myinput = input("请输入需要修改的配置文件的内容：") #输入的是字符串类型的字典
            try:
                mydic = json.loads(myinput)  #把输入的字符串转换成字典  注意方法是loads而不是load
            except Exception: #异常处理，如果输入的字典格式不对，例如中文标点之类，要求用户重新输入
                myinput = input("\033[31;1m字典输入格式不正确，请重新输入需要更新的内容：\033[31;1m")
            ret = charuhang01.zhuanhuan2(mydic)  #往列表删除目标行.mydic是实际参数
            charuhang01.writenew(ret)   #将修改后的列表写入到新的文件
            ret3 = charuhang01.zhuanhuan(mydic)  #往列表添加目标行.mydic是实际参数
            charuhang01.writenew(ret3)   #将修改后的列表写入到新的文件
            #函数2-writenew将函数1-zhuanhuan的返回值，作为参数传入
            print("\033[32;1m配置文件修改行成功\033[31;1m")
            break
        elif choice == "4":  #查询配置文件指定标题行下的内容
            # print("\033[35;1m查看功能还未提供，敬请期待\033[0m")
            myinput = input("请输入需要查询的配置文件的内容：") #输入的是字符串类型的字典
            try:
                mydic = json.loads(myinput)  #把输入的字符串转换成字典  注意方法是loads而不是load
            except Exception: #异常处理，如果输入的字典格式不对，例如中文标点之类，要求用户重新输入
                myinput = input("\033[31;1m字典输入格式不正确，请重新输入需要查询的内容：\033[31;1m")
            ret = charuhang01.cal_index(mydic)  #往列表查询目标行
            # charuhang01.writenew(ret)   #将修改后的列表写入到新的文件
            #函数2-writenew将函数1-zhuanhuan的返回值，作为参数传入
            print("\033[32;1m配置文件指定字段查看成功\033[31;1m")
            break
        elif choice == "5":
            print("\033[36;1m退出系统\033[0m")
            break
        else:  #如果输入的不是a或者c
            print("\033[31;1m您输入的指令无效，请重新输入\033[0m")
            continue  #跳出循环本次迭代










