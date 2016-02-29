__author__ = 'Administrator'
# -*- coding:utf-8 -*-

#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
用户登陆功能实例
1、获取db文件中所有的用户信息
2、比较用户信息
    如果用户名不存在，则直接退出
    如果用户名存在
        检测密码，如果密码存在，则提示登陆成功，并将登陆错误次数重置为 0 ，修改内存中的字典中记录的登陆错误次数。（并写入文件）
        如果密码不存在
            修改内存中的字典中记录的登陆错误次数

        将最新的登陆错误次数和对应用户信息写入文件

"""


# 读取用户信息到 user_info_list 中
read = file('db1','r')
user_info_list = read.readlines()
read.close()

# 处理 user_info_list，以便之后的用户名和密码比较
# 处理后的结果： user_info_dict = {'alex': {'pwd': '112233', 'times': 0}, 'eric': {'pwd': '111111', 'times': 0}}
user_info_dict = {}
for item in user_info_list:
    user_info = item.split(';')
    user_info_dict[user_info[0]] = {'pwd': user_info[1], 'times': int(user_info[2].strip())}

while True:
    username = raw_input('请输入用户名：')
    #用户名为空
    if len(username) == 0:
        print "\033[31;1m用户名不能为空\033[0m"
    # 用户名不存在
    elif username not in user_info_dict.keys():
        print '\033[31;1m用户名不存在，请重新输入！\033[0m'
    # 用户名存在
    else:
        # 判断登陆次数
        if user_info_dict[username]['times'] >=3:
            print '\033[31;1m账户已经冻结，请联系管理员\033[0m'
            break
        else:
            # while True:
            pwd = raw_input('请输入密码：')
            if user_info_dict[username]['pwd'] == pwd:
                # 如果登陆成功，将登陆次数重置为 0
                user_info_dict[username]['times'] = 0
                print '\033[32;1m恭喜您 %s，登陆成功\033[0m' % username
                break
            else:
                # 如果登陆失败，将登陆次数加一
                user_info_dict[username]['times'] += 1
                times = user_info_dict[username]['times']
                left_times = 3- times
                if left_times ==0:
                    print '\033[31;1m账户已经冻结，请联系管理员\033[0m'
                    break
                else:
                    print "\033[31;1m密码输入错误，请重新输入，您还有 %s 次尝试机会，输入密码错误3次，" \
                          "账号锁定，密码正确，错误登录次数置为0\033[0m" % (left_times)
# 将最新的登陆次数写入文件
# (写文件这段代码需要写在循环之外的最后面，如果写在65行或者64行同级缩进，会出现登录成功后，登录次数没有及时写入到文件的情况)
temp_list = []
for key, value in user_info_dict.items():
    temp = "%s;%s;%d" % (key, value['pwd'], value['times'])
    temp_list.append(temp)
temp_str = "\n".join(temp_list)
w_obj = file('db1', 'w')
w_obj.write(temp_str)
w_obj.flush()
w_obj.close()


