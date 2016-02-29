__author__ = 'Administrator'
# -*- coding:utf-8 -*-

#!/usr/bin/env python
# -*- coding:utf-8 -*-

# login整体思路
# 1 用户名为空len(用户名)==0
# 2 用户名不存在
# 3 用户名存在
#   1 用户名和密码都正确 登录次数改为0 break退出当前循环 sys.exit()退出整个程序
#   2密码错误 登录次数+1(列表中)  将修改后的列表
#    6 列表的内容修改后，通过"|"作为连接符join成字符串
# #    7 将字符串作为元素添加到空白列表
# #    8 遍历for结束，内存中的列表已经是修改后的登录次数
# #    9 光标回到文件最开始seek(0)
# #    10 以换行\n作为连接符，将列表变成大字符串
# #    11write写入大的字符串到文件对象
# #    12 关闭文件对象

# 写文件整体思路
# 1、读文件到内存
#    1 读写模式r+打开文件
#    2 for遍历文件
#    3 去字符串的换行符strip
#    4 用|作为分隔符，拆分字符串split成列表
#    5 通过列表的最后一项list[-1]转换成int后 加1后，再转换成字符串
#    6 列表的内容修改后，通过"|"作为连接符join成字符串
#    7 将字符串作为元素添加到空白列表
#    8 遍历for结束，内存中的列表已经是修改后的登录次数
#    9 光标回到文件最开始seek(0)
#    10 以换行\n作为连接符，将列表变成大字符串
#    11write写入大的字符串到文件对象
#    12 关闭文件对象
# 2 在内存中通过列表修改登录次数
# 3 将修改后的列表用换行符转换成大字符串，写入到文件

# 整体思路：
# 1、外层定义一个while True死循环，用于用户输入用户名（用户名输入不对的话，会一直要求输入）
#
# 2、初始工作
#    1、定义2个空的列表，空列表1计划把文件中的2行字符串，分别作为列表存到这里列表变量中，
#       遍历这个列表后，用于通过索引号取出用户名和密码字段，用于和用户输入的用户名和密码对比进行判断
#
#        空列表2计划将修改登录次数后的2个字符串作为元素，写入到这个列表变量中，最终用于写到文件中
#    2、定义一个flag，当用户输入的用户名==列表中的索引号是0的用户名的时候，flag=1
#       那么flag =0就代表用户输入的用户名不存在
#    3、读写模式打开文件对象（先读后写）
#       1、读文件，遍历文件对象，将字符串strip去换行符后，用split拆分成列表；
#       2、将列表[-1]转换成int，便于登录次数计算
#       3、将把文件中的2行字符串，分别作为列表添加这里空列表1变量中
#    4、用户输入用户名raw-input
#    5、几个场景
#         # 1 用户名为空：len(用户名)==0
# 		# 2 用户名不存在：flag =0
# 		# 3 用户名存在:  用户输入的用户名==子列表[0]
# 			#   a 用户名和密码都正确 登录次数改为0 break退出当前循环 sys.exit()退出整个程序
# 			#   b 密码错误 登录次数+1(列表中)  将修改后的列表转换成字符串，写入到文件
#
# 3、遍历内部含有2个列表的列表
#
# 4、内层定义一个while True死循环，用于用户输入密码（密码输入不对的话，会一直要求输入，直到break跳出内循环）
#    1、密码输入raw_input(或者getpass-密码看不见)
#    2、密码判断（用户名正确的前提下）
#       1、分支1：密码正确且登录次数小于3，提示登录成功；
# 	  2、分支2：登录次数大于等于3，提示用户锁定；
# 	  3、分支3、密码错误（登录次数+1）,提示还有几次登录机会；
#    3、将登录次数转换成str
#    4、将修改后的字符串添加到空列表2
#
# 5、判断用户不存在 if flag == 0  ，提示用户不存在，用户重新输入，回到外循环while
#
# 6、如果用户存在的话
#    1、光标seek(0)到文件最开始
#    2、将修改了登录次数的列表（空列表2中的数据） ，用换行符\n 连接join成一个多行字符串
#    3、write这个字符串到文件对象
#    4、关闭文件对象
#    5、break 跳出外循环



# import getpass
import sys

while True:#死循环，用于61行输入用户名（用户名输入不对的话，会一直要求输入）
    old_user_list = []  #计划把文件中的2行字符串，分别作为列表存到这里列表变量中
    new_user_list = []  #计划将修改登录次数后的2个字符串作为元素，写入到这个列表变量中
    # # 定义一个标识数，来判断用户是否存在
    flag = 0   #0的话代表用户名不存在  不是0代表用户名存在（首先用户存在的时候，就将flag置为1；
    # --用户输入的==子列表的第一个元素（文件中的用户名）
    # 那么flag==0的时候，就是用户不存咋）
    f = file('userinfo.txt', 'r+')  #读写模式打开文件（先将文件的字符串读入到内存，转换成列表后修改登录次数
    #然后将修改后的字符串seek(0)到文件开始，覆盖写入修改后的字符串到文件 ）
    # 从文件中读取用户信息保存到用户列表内
    for line in f:   #遍历文件（读取文件字符串到内存 1拆成列表 2将登录次数转换成int，便于计算 3、将2个列表作为元素添加到空列表）
        # print line,  #"jack;123;3"
        tmp_line_list = line.strip().split(';')  #将字符串去掉换行符后，用";"作为分隔符，拆分成列表
        # 将用户登录错误次数转为int类型,如果转换失败，将用户锁定
        # print tmp_line_list  #['jack', '123', '0']  ['tom', '123', '0']
        try:
            tmp_line_list[-1] = int(tmp_line_list[-1])  #将列表的最后一项-登录次数转换成int，用于计算
        except ValueError, e:
            tmp_line_list[-1] = 3
        old_user_list.append(tmp_line_list)  #将2个列表作为元素添加到空白列表中
        # print old_user_list   #[['jack', '123', 0], ['tom', '123', 0]]
    username = raw_input('请输入用户名: ').strip()  #将输入的用户名去掉2边空格
    if len(username) == 0:  #判断输入的用户名是否为空
        print '\033[31;1m用户名不能为空！\033[0m'  #提示有颜色
        continue  #跳出当次迭代（当次循环），回到最外层的while死循环，重新输入用户名

    for user_line in old_user_list:  #遍历内部含有2个列表的列表，和while和for循环有点区别
        #print user_line  #['jack', '123', 0] ['tom', '123', 0]
        if username == user_line[0]:  #判断输入的用户名是否等于子列表的第一个元素（文件中的用户名）
            # # 用户存在标识数加1
            # print user_line[0]
            flag = 1
            while True:  #定义一个内部的while死循环，用于73行输入密码（密码输入不对，会一直要求输入，除非break）
                password = raw_input('请输入密码: ')  #输入密码
                if password == user_line[1] and user_line[-1] < 3: #判断输入的密码等于子列表的第2个元素（文件中的密码）且登录次数小于3
                    # 用户登录成功后将错误次数重置为0
                    # print user_line[1]
                    user_line[-1] = 0   #将登录次数置为0
                    print '\033[32;1m登录成功，欢迎%s!\033[0m' % username #提示成功，提示语有颜色,成功显示绿色（亮青色）
                    break  #跳出内部的while循环（不会再要求输入密码） 走到106行
                    # sys.exit()  #引发一个 SystemExit异常，若没有捕获这个异常，Python解释器会直接退出
                elif user_line[-1] >= 3:  #如果登录次数大于等于3
                    print '\033[31;1m用户"%s"已锁定，请联系管理员!\033[0m' % username  #提示语有颜色，失败显示红色
                    # time.sleep(3)
                    break
                    #sys.exit() #引发一个 SystemExit异常，若没有捕获这个异常，Python解释器会直接退出
                else:  # 用户名正确，密码错误
                    # 用户名正确，密码错误，错误次数加1
                    user_line[-1] += 1  #子列表的最后一项-登录次数加1
                    # 获取剩余尝试次数
                    rest_nums = 3 - user_line[-1]  #定义剩余的尝试次数
                    # 如果尝试次数为0，则不再允许尝试
                    if rest_nums == 0:  #如果剩余尝试次数是0
                        print '\033[31;1m用户"%s"已锁定，请联系管理员!\033[0m' % username  #失败显示红色
                        flag = 3
                        break#跳出内部的while循环（不会再要求输入密码） 走到106行
                    else:
                        print "\033[31;1m密码错误！您还可以尝试%d次，错误3次后用户将被锁定，登录成功后错误次数将重置！\033[0m" % rest_nums
                        #失败显示红色  这里没有break，会重复3次提示输入密码，直到锁定
                        # continue   这里可以注释continue，因为内循环中continue后没有代码，加和不加效果一样
        # 将用户错误次数转为str类型
        user_line[-1] = str(user_line[-1])  #前面56行转换成数字，为了计算，现在要存储到文件，应该转换成str类型
        # 将用户信息转为以“；”分割的字符串，添加到新的用户列表
        new_user_list.append(';'.join(user_line))  #将修改后的字符串添加到新的空白列表
        # print new_user_list  #['jack;123;0', 'tom;123;0']
    if flag == 0:  #flag=0 标识用户名不存在
        print '\033[31;1m用户名不存在，请重新输入！\033[0m'   #重新输入用户名，到了58行  失败显示红色
    else:   #表示用户名存在的所有情况，将修改完登录次数的列表转换成字符串写入到文件
        f.seek(0)   #回到文件最开始处，将内存中存储的字符串写入到文件对象，覆盖之前的文件内容
        # 将新的用户列表转为以“\n”为分割的字符串，写入到用户信息文件
        f.write('\n'.join(new_user_list))  #字符串在文件中是分行存储的，所以用\n换行
        # print '\n'.join(new_user_list)
        #jack;123;0\ntom;123;0
        f.flush()
        f.close()  #关闭文件对象
        break  #跳出外循环while
        #sys.exit() #引发一个 SystemExit异常，若没有捕获这个异常，Python解释器会直接退出
        #跳出外循环while
    # f.seek(0)    #用户名不存在的时候，执行下述代码，此处代码可以注释
    # # 将新的用户列表转为以“\n”为分割的字符串，写入到用户信息文件
    # f.write('\n'.join(new_user_list))
    # # print '\n'.join(new_user_list)
    # f.flush()
    # f.close()





























