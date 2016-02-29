__author__ = 'Administrator'
# -*- coding:utf-8 -*-


# 三级菜单涉及知识点：
# 1、字典的取值方式：字典通过key取值  dict[用户输入省名字]（遍历可以得到地市列表）   dict[用户输入省名字][用户输入地市名字]（遍历可以得到区县列表）
# 2、多次嵌套循环的跳出：按q退出程序
# 3、颜色提示语
#    加颜色：正常绿色 失败红色
#    '\033[32;1m登录成功，欢迎%s\033[0m'     --绿色
#    '\033[31;1m用户"%s"已锁定，请联系管理员\033[0m'   --红色

# 三级菜单整体思路：
# 1 定义一个字典，存储省市列表
# 2 遍历字典，输出省市列表
# 3 定义2个循环，外循环用于用户输入省市名字，内循环用于用户输入地市名字
#   1 用户输入的省市名字在字典中，通过遍历dict[用户输入省名]，得到地市列表
#      1  判断用户输入的地市名字在字典dict[用户输入省名]中,
#         通过遍历列表dict[用户输入省名][用户输入地市名]，得到区县列表
#         1、提示用户输入指令，q退出整个程序break （需要退出2层循环,break_flag）
#         2、b回到上一级菜单，continue
#         3、输入q或者b之外的无效字符，提示重新输入continue
#      2  用户输入的地市名字不在字典dict[用户输入省名]中，continnue，提示用户重新输入
#   2 用户输入的省市名字不在字典中，提示用户重新输入，错误3次后，程序退出





#定义一个字典，构造数据
city_map = {
    "湖北":{"武汉":["武昌","汉阳","汉口"],
            "黄冈":["黄州","红安","麻城"]},
    "吉林":{"长春":["高新区","南关区"],
            "四平":["东区","西区"]},
}

break_flag = False #外循环跳出标识
times = 0  #定义省名输入次数
for i in city_map:  #打印省列表，遍历字典
    print i   #吉林 湖北

for j in range(3): #外循环（固定循环次数3次），输入省市，输入错误3次后，程序退出
    prov_input = raw_input("请输入你要查看的省市:") #要求用户输入省名字
    if prov_input in city_map: #如果用户输入的省名字在字典中
        # sheng_name = city_map[prov_input]  #字典
        # city_name = sheng_name.keys()
        # print sheng_name
        while True:  #内循环，输入地市，死循环，地市输入错误，会一直要求用户输入，直到break
            for i in city_map[prov_input]:   #遍历字典（通过用户输入的省名字作为字典的key）dict[用户输入省名]
                print i #会一直都打印地市列表
            city_input = raw_input("请输入你要查看的地市:") #要求用户输入地市名字
            if city_input in city_map[prov_input]: #如果用户输入的地市名字在字典中（通过用户输入的省名字作为字典的key）
                quxian_list = city_map[prov_input][city_input]  #区县列表（通过dict[用户输入省名][用户输入地市名]来表示区县列表）
                for i in quxian_list:#遍历区县列表
                    print i
            else:#如果用户输入的地市名字不在字典中
                print "\033[31;1m输入的地市不对，请重新输入\033[0m" #红色字体提示不对
                continue  #跳出当次迭代，回到输入地市名字处 26行
            tuichu = raw_input("请问是否退出？按q退出程序，按b回到上一级菜单") #要求用户输入指令，退出程序还是回到上一级
            if tuichu == "q":  #输入q，
                break_flag = True #退出内循环前，先把break_flag置为True 43行
                break  #退出内循环
            elif tuichu == "b": #输入字符"b"
                continue  #跳出当次迭代，回到输入地市名字处，26行
            else:  #输入的不是q也不是b，输入的其他
                print "\033[31;1m你输入的信息有误，请重新输入\033[0m" #红色字体提示指令不对
                continue  #跳出当次迭代，回到输入地市名字处，26行
        if  break_flag:  #36行
            break  #退出外循环
    else: ##如果用户输入的省名字不在字典中
        times +=1  #错误次数=1
        left_times = 3- times  #计算剩余尝试次数
        if times == 3: #错误次数=3
            print "\033[31;1m3次输入错误，程序退出\033[0m"  #红色字体提示程序退出
        else: #错误次数1,2
            print "\033[31;1m省市输入错误，请重新输入,您还有%s次输入机会，3次输入错误，程序将退出\033[0m" % left_times
            #红色字体提示还有几次输入机会
# else:
#     print "3次输入错误，程序退出"
