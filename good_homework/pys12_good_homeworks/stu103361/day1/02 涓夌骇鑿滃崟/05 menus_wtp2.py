__author__ = 'Administrator'
# -*- coding:utf-8 -*-

city_map = {
    "湖北":{"武汉":["武昌","汉阳","汉口"],
            "黄冈":["黄州","红安","麻城"]},
    "吉林":{"长春":["高新区","南关区"],
            "四平":["东区","西区"]},
}

break_flag = False
times = 0

for i in city_map:
    print i  #吉林 湖北

for j in range(3):
    prov_input = raw_input("请输入省市名字:")
    # for city_name in city_map[prov_input]:
    #     print city_name
    if prov_input in city_map:
       while True:
            for city_name in city_map[prov_input]:
                print city_name
            city_input = raw_input("请输入地市名字:")
            if city_input in city_map[prov_input]:
                for quxian in city_map[prov_input][city_input]:
                    print quxian
            else:
                print "输入的地市名字不对，请重新输入"
                continue
            tuichu = raw_input("你确认退出么？输入b返回上一级，输入q退出程序")
            if tuichu == "b":
                continue
            elif tuichu == "q":
                break_flag = True
                break
            else:
                print "无效的输入，请重新输入"
                continue
    else:
        times += 1
        left_times = 3-times
        if times ==3:
            print "3次输入错误，程序退出"
        else:
            print "省市输入错误，请重新输入，您还有%s次输入机会，3次输入错误，程序退出" % left_times
    if break_flag:
        break
# else:
#     print "3次输入错误，程序退出"