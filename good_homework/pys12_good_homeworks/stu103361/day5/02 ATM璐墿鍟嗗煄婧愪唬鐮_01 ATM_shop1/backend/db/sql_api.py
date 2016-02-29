__author__ = 'Administrator'
#-*- coding:utf-8 -*-
import sys
import os

import json

# #需求：直接执行sql_api.py，这个文件导入了config下的setting(需要将config的上一级目录dj加入到环境变量)
# #需要将sql_api.py的上一级db的上一级backend的上一级dj的路径加到环境变量中，默认的环境变量是sql_api.py当前的绝对路径的上一级目录db
# #D:\PycharmProjects\s12\day5_0130\ketang\dj\backend\db\sql_api.py  当前的绝对路径
#
# #1得到当前py文件的绝对路径  os.path.abspath
# print(os.path.abspath(__file__))#可以取出当前文件的绝对路径
# ##D:\PycharmProjects\s12\day5_0130\ketang\dj\backend\db\sql_api.py
#
# #2得到当前py文件的上一级目录 os.path.dirname
# print(os.path.dirname(os.path.abspath(__file__)))  #返回sql_api.py所在的目录  其实就是os.path.split(path)的第一个元素
# #D:\PycharmProjects\s12\day5_0130\xiaojie\dj\backend\db
#
# #3得到当前py文件的上2级目录 os.path.dirname
# print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# #D:\PycharmProjects\s12\day5_0130\xiaojie\dj\backend
#
# #4得到当前py文件的上3级目录 os.path.dirname
# print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# #D:\PycharmProjects\s12\day5_0130\xiaojie\dj
#
# # os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))可以取出
# # D:\PycharmProjects\s12\day5_0130\ketang\dj这个路径
# # D:\PycharmProjects\s12\day5_0130\ketang\dj这个路径这个绝对路径不能直接写死到环境变量，避免文件拷贝到别的
# # 地方，还是执行这个绝对路径
# #需要将路径D:\PycharmProjects\s12\day5_0130\ketang\dj添加到环境变量sys.path中
#
#
#
#
# print(sys.path) ##默认路径是当前py文件的父目录
# #将环境变量加到sys.path中
# print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(os.path.dirname(os.path.abspath(__file__)))
# print(os.path.abspath(__file__)) #绝对路径 D:\PycharmProjects\s12\day5_0130\xiaojie\dj\backend\db\sql_api.py
# print(__file__) #D:/PycharmProjects/s12/day5_0130/xiaojie/dj/backend/db/sql_api.py

#将当前的py文件的上3级目录（3个os.path.dirname）添加到环境变量
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#一个os.path.dirname显示上一级目录，3个os.path.dirname显示上三级目录
sys.path.append(base_dir)
# print(sys.path)
#['D:\\PycharmProjects\\s12\\day5_0130\\xiaojie\\dj\\backend\\db',   ---原来的
# 'D:\\PycharmProjects', 'C:\\Python35\\python35.zip', 'C:\\Python35\\DLLs',
# 'C:\\Python35\\lib', 'C:\\Python35', 'C:\\Python35\\lib\\site-packages',
# 'D:\\PycharmProjects\\s12\\day5_0130\\xiaojie\\dj']   --新添加进来的
#linux下打印相对路径（文件名）

from config import settings

def db_auth(configs):  #数据库登录验证函数，形参是configs
    if configs.DATABASE["user"] == "root" and configs.DATABASE["password"] == "123":
        # print("db登录验证通过")
        return True   #返回True
    else:
        print("db登录验证失败")

#数据库接口
def select(table,column): #查询函数,参数是表名字和字段名字
    if db_auth(settings): #实参是setting的字典（先验证数据库是否登录成功，验证成功，才能返回字典信息）
        #验证成功，返回True，下面的才会执行，验证失败，返回None，下面的就不执行（select函数返回None）
        if table == "shop":  #实参是表名
            # 如果实参不是"user_table",下面的代码也是不执行，select默认返回None
            # user_info ={   #正常来说，user_info的信息应该从数据库查询出来，这里没有实际数据库，直接把信息存在字典中
            #     #这些sql语句有dba编写
            #     "001":["alex",22,"engineer"],
            #     "002":["longge",43,"chef"],
            #     "003":["xiaoyun",23,"13baoan"]
            #             }
            #读商品文件
            f = open("shop.txt","r+")
            for i in f:
                user_info = json.loads(i)   #经过json.loads转换后，读取的字符串转换成了字典
                # user_info = str(user_info)
            #     print(user_info)  #{"k1": "v1", "k2": "v2"}
            # print(type(user_info)) #<class 'dict'>
            f.close()

            #这个地方，将文件中的字符串loads成字典，商品表和余额2个字典
            return user_info  #将字典的信息返回给select的调用者


        if table == "yue":
            pass
            #读商品文件
            f = open("username1.txt","r+")
            for i in f:
                user_info_yue = json.loads(i)   #经过json.loads转换后，读取的字符串转换成了字典
                # user_info = str(user_info)
            #     print(user_info)  #{"k1": "v1", "k2": "v2"}
            # print(type(user_info)) #<class 'dict'>
            f.close()

            #这个地方，将文件中的字符串loads成字典，商品表和余额2个字典
            return user_info_yue  #将字典的信息返回给select的调用者

        if table == "jilu":
            pass
            #读商品文件
            f = open("chongzhi.txt","r+")
            for i in f:
                jilu_info = json.loads(i)   #经过json.loads转换后，读取的字符串转换成了字典
                # user_info = str(user_info)
                # print(jilu_info)  #{"k1": "v1", "k2": "v2"}
            # print(type(user_info)) #<class 'dict'>
            f.close()

            #这个地方，将文件中的字符串loads成字典，商品表和余额2个字典
            return jilu_info  #将字典的信息返回给select的调用者

        if table == "username":
            pass
            #读商品文件
            f = open("username1.txt","r+")
            for i in f:
                user_info_mima = json.loads(i)   #经过json.loads转换后，读取的字符串转换成了字典
                # user_info = str(user_info)
                # print(user_info)  #{"k1": "v1", "k2": "v2"}
            # print(type(user_info)) #<class 'dict'>
            f.close()

            #这个地方，将文件中的字符串loads成字典，商品表和余额2个字典
            return user_info_mima  #将字典的信息返回给select的调用者
#步骤1 user_main001导入 backend.logic下的handles002（逻辑文件），调用handle 002的home函数---查看首页，打印首页信息
#步骤2 handles002导入backend.db.sql_api 003(数据库接口文件)，调用sql_api 003的select函数
#步骤3 backend.db.sql_api 003导入 from config import settings 004，
#步骤4 from config import settings 004下值保存数据了的jdbc连接信息