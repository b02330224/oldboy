__author__ = 'Administrator'
#-*- coding:utf-8 -*-

#功能描述
#1、实现计算器的加减乘除四则运算，并且可以处理小括号优先级；
#2、计算器使用前，要求用户登录，使用用户名:jack或者tom,密码都是：123登录后，才能使用计算器；
#   如果账号锁定，请收到修改username.txt的错误登录次数为0，解锁
#   登录失败，不允许使用计算器，通过带参数的装饰器实现使用前的登录验证

#整体思路：
# 先计算不带括号的表达式，再计算带括号的表达式
# 1 乘除函数，用于处理表达式中的乘除法（去掉乘除符号），参数是列表
#   1 正则查找类似90.1*90.2  90.1*-90.2 90.1*+90.2这样两个数相乘的情况，search找出左边第一个符合要求的字符串存在mid变量
#   2 通过split将表达式分成前中后3部分，第三个参数是1
#   3 计算中间部分mid的值
#   4 将前中（mid计算后的值）后三部分重新拼接成一个新的表达式
#   5 递归调用自己，参数是新的表达式
#   6 递归退出条件，当表达式中没有乘除符号的时候，return None
# 2 加减函数，乘除处理完毕后，用加减函数处理加减法（去掉加减符号），参数是列表
#   1 正则查找类似90.1-90.2 90.1+90.2这样两个数相加减的情况，search找出左边第一个符合要求的字符串存在mid变量
#   2 通过split将表达式分成前中后3部分，第三个参数是1
#   3 计算中间部分mid的值
#   4 将前中（mid计算后的值）后三部分重新拼接成一个新的表达式
#   5 递归调用自己，参数是新的表达式
#   6 递归退出条件，当表达式中没有加减符号的时候，return None
#   7 和乘除函数不同的是，加减函数还需要替换表达式中的++ -- +- -+符号
#   8 还需要将数前面的-负号单独提取出来，---就相当于负数 ----就相当于整数
#     需要用到将待计算的表达式，作为列表的第一个元素，根据列表的第二个元素（负号每递增一次，第二个元素自增1）
#   9 计算的时候，需要先将数转换成float类型
# 3 计算函数，依次调用乘除函数和加减函数，对表达式进行运算，参数是表达式
#   1、根据符号提取的个数是奇数还是偶数，奇数就是负数，偶数就是整数
# 4 去小括号函数，上述3个函数都没有涉及到小括号，这个函数专门用来处理小括号（一层层去掉小括号），参数是表达式
#   去小括号函数，在计算小括号内的值的时候，调用计算函数
#   1 正则查找类似（-90.1*90.2+1）这样小括号开头，小括号结尾，中间不包含小括号的情况，
#     search找出左边第一个符合要求的字符串存在mid变量
#   2 通过split，用查找到的字符串作为分隔符，将表达式分成前中后3部分，第三个参数是1
#   3 计算中间部分mid的值（通过调用计算函数实现）
#   4 将前中（mid计算后的值）后三部分重新拼接成一个新的表达式
#   5 递归调用自己，参数是新的表达式
#   6 递归退出条件，当表达式中没有乘除小括号的时候，直接调用计算函数，return最后计算的值给主函数main
# 5 main函数，定义表达式，将表达式中间的空格去掉，调用去括号函数，返回去括号函数的return值
# 6 用eval函数验证最后的计算结果是否正确

#踩过的坑：
#1 "\(([\*\/\+\-]*\d+\.*\d*){2,}\)" 匹配小括号的时候，{2,}前面的小括号少了或者写成了中括号
#2 乘除法计算完毕后，递归默认返回的是None，如何将乘除法计算后的值，传给加减法
# （解决办法：将表达式作为列表的第一个元素传入,通过2个return将乘除计算的结果返回，传给加减法）
#3 71 113 124行，通过列表的第一个元素，将乘除后的表达式传递给加减，将加减后的字符串传递给计算函数的return值
    #关键点，这里如果不用列表的形式，直接表达式的话，会出现 ValueError: could not convert string to float:
    #如果是字典的第一个元素的话，前面的乘除法，修改了字典的第一个元素的值，变成了只含有加减号的表达式，在加减法函数，
    #接受的就是指含有加减号的，计算完毕后，字典的第一个元素的值变成了一个字符串，转换成float后，就正确了
#4  乘除函数计算完毕后，如何将乘除法计算后的值，传给加减法
#   办法1：乘除函数通过2个return，将去掉乘除符号的表达式，传给加减函数：
#     第一个rerurn，递归出口，最后没有乘除符号的时候，将去掉乘除符号的表达式，return给他的上一层调用者
#      第二个rerurn，退出递归的时候，接受最后去掉乘除符号的表达式，依次传给它的上一层调用，最后返回去掉乘除的表达式
#给计算函数的264行，加减函数的参数就是这个去掉乘除符号的表达式
#    办法2：乘除函数，递归出口，最后没有乘除符号的时候，直接return，退出递归循环
#       （注意，这里的return不上返回None，而是终止函数）
#         递归调用乘除函数的时候，也不return递归函数的值，219行chengchu(expr_list)前面不用return
#          执行乘除函数的目的，在这里不上为了将去掉乘除符号的表达式return返回，而是用退出递归前，递归计算后的表达式来修改计算函数268行
#          中的expr_list，当这个expr_list修改后，加减函数的参数就是expr_list，这样加减函数的参数就是依据去掉乘除符号的表达式了
#5 递归的return总结：return 就是跳出函数并返回值，如果没有返回值就跳出函数

#涉及的知识点
#1正则
#  1匹配小括号开头，小括号结尾，直接不包含小括号，只包含运算符和数字
#  2 search匹配90.1*90.2  90.1*-90.2两个数相乘除
#    split用匹配到的字符串，拆分表达式成前中后3部分
#    计算中间mid的值
#    重新拼接成新的表达式
#    递归调用函数自己，参数是新的表达式
#  3匹配90.1+90.2  90.1-90.2两个数相加减
#  4匹配计算表达式不能有大小写字母或者特殊字符
#2递归
# 1小括号递归，递归退出的条件是，没有小括号符号，直接调用计算函数，return计算函数的返回值
# 2乘除递归，递归退出的条件是，没有乘除符号，return None
# 3加减递归，递归退出的条件是，没有加减符号，return None
#3特殊处理
# 1 ++ -- +- -+都成立成单符号 in replace
# 2表达式中的空格去掉 sub
# 3提取数最前面的负号  ---就是负数  ----就是正数 divmod
# 4去掉mid两端的小括号，切片
#4带参数的装饰器，实现计算器使用前的登录验证

import re #导入正则模块

# #2函数带参数的装饰器
# def login(func):  #func=qukuohao
#     def inner(*args,**kwargs):  #inner() = qukuohao()
#         print("用户名密码验证")   #用户名密码验证功能-函数
#         func(*args,**kwargs)   #func() = qukuohao()   #执行tv查看函数  15行
#     return inner   #inner = qukuohao

# def Login(): #登录,执行功能函数前，先登录
#     print('before')   #相当于在查看tv页面前，先执行登录用户名密码验证

def Login():
    print("要使用计算器，请先验证用户名密码，登录成功后，才能使用")
    f = open("username.txt","r+")  #读写模式打开文件
    # for i in f:
    #     line_list = i.strip().split("|")  #错误登录次数需要转换成int，计算
        # print i.strip().split("|")  #['tom', '123', '0']

    #2构造字典
    break_flag = False  #跳出外循环标识
    user_dict = {}  #空列表
    for i in f:  #遍历文件
        line_list = i.strip().split("|")  #['tom', '123', '0']
        try: #异常处理，如果错误登录次数不少数字，就赋值成数字3，锁定
           line_list[-1] =int(line_list[-1])
        except:
           line_list[-1] = 3
        user_dict[line_list[0]] = {"pwd":line_list[1],"times":line_list[-1]} #错误登录次数需要转换成int，计算
        # print user_dict  #{'jack': {'pwd': '123', 'times': 0}, 'tom': {'pwd': '123', 'times': 0}}

    #3逻辑判断
    while True: #判断用户名，外循环，用于输入用户名
        username = input("请输入用户名:")
        if len(username) == 0:  #判断用户名是否正确
            print("\033[31;1m用户名不能为空\033[0m")
        elif username not in user_dict:
            print("\033[31;1m用户名不存在\033[0m")
        else:
            if user_dict[username]["times"] >= 3 :  #判断错误登录次数是否大于等于3
                print("\033[31;1m账号锁定，请联系管理员\033[0m")
                break
            else:
                while True: #内循环，用于输入密码
                    passwd = input("请输入密码:")
                    if passwd == user_dict[username]["pwd"]:
                        # print user_dict[username]  #{'pwd': '123', 'times': 0}
                        #user_dict[username]["pwd"] 指的是密码
                        # user_dict[username]["times"] 错误登录次数
                        user_dict[username]["times"] =0
                        print("\033[32;1m登录成功\033[0m",username)
                        break_flag = True
                        # break  #跳出内循环
                        return  #这里返回的是None，计算器函数可以正常执行--162行
                    else: #密码不对，但是错误登录次数<3
                        user_dict[username]["times"] += 1
                        times = user_dict[username]["times"]
                        # times+= 1
                        left_times = 3- times
                        if left_times ==0:
                            print("\033[31;1m账号锁定，请联系管理员\033[0m")
                            break_flag = True
                            break #跳出内循环
                            # return "\033[31;1m账号锁定，请联系管理员1\033[0m" #这里返回的不是None，162行函数return终止了，计算器函数就不执行了
                        else:
                            print("\033[31;1m密码输入错误，请重新输入，您还有 %s 次输入机会，3次密码输入错误，账号锁定" \
                                  "密码输入正确后，错误登录次数重置为0\033[0m" % (left_times))
                            continue #跳出内循环当次迭代
                if break_flag:  #跳出外循环，和39行while同一级
                    break  #跳出外循环
    temp_list= []  #定义空列表
    for k,v in user_dict.items():  #遍历字典的项目items()  key value（k v）--items（）必须
        mystr = "%s|%s|%s" % (k,v["pwd"],str(v["times"])) #用k v模式拼接字符串 (将错误登录次数转换成字符串，用于写入)
        # print mystr
        temp_list.append(mystr)  #将字符串作为元素添加到空列表
        # print temp_list
    f.seek(0)  #回到文件最开始
    temp_str = "\n".join(temp_list)  #将列表的2个元素用换行符分隔，转换成字符串
    # f = open('db1', 'w')
    f.write(temp_str) #写入字符串
    f.flush()  #关闭文件前，最好带上（刷新缓存）
    f.close() #关闭文件对象（句柄）
    return "登录失败原因"

def Errorhandle(): #执行功能函数后，处理错误或者提示错误
    print('after:计算器使用前，需要登录，使用后的收尾工作，留作后续扩展，敬请期待')   # #相当于在查看tv页面后，执行收尾工作（例如退出用户名登录）


#2默认装饰器（框架）--一个函数被多个装饰器装饰（这里不必写2个装饰器，只需要写2个函数即可，4,7行）
def Filter(before_func,after_func):
    def outer(main_func):  #func=tv
        def inner():  #inner() = tv()
            # print("用户名密码验证")   #用户名密码验证功能-函数
            # func(request,kargs)   #func() = tv()   #执行tv查看函数  15行
            before_result = before_func()  #登录密码验证
            if(before_result != None):  #登录有return，说明登录失败，自己定义的，功能函数不执行
                return before_result;    #返回登录错误信息

            main_result = main_func()  #业务函数 index
            if(main_result != None):  #业务函数有return，说明业务函数失败，自己定义的，功能函数不执行
                return main_result;   #返回业务函数错误信息

            after_result = after_func()  #收尾函数
            if(after_result != None): ##执行业务函数后，处理一些收尾工作
                return after_result;   #返回收尾函数错误信息
        return inner   #inner = tv
    return outer

# my_list = []
def chengchu(expr_list):  #参数：列表（表达式作为列表的第一个参数） 乘除函数
    expr = expr_list[0]  #列表的第一个元素是待计算的表达式
    mch = re.search("\d+\.*\d*[\*\/]+[\+\-]?\d+\.*\d*",expr)  #90.1*90.2  90.1*-90.2  90.1*+90.2 匹配2个数相乘除的字符串
    # print(mch)
    if not mch: #递归出口，最后没有乘除符号的时候，将去掉乘除符号的表达式，return给他的上一层调用者
        return expr_list  #
    mid = re.search("\d+\.*\d*[\*\/]+[\+\-]?\d+\.*\d*",expr).group() #匹配乘除法的两个数想乘除,取左边第一个符合要求的字符串
    #计算mid
    if len(mid.split("*"))>1:
        n1,n2 = mid.split("*")
        value = float(n1)*float(n2)
    else:
        n1,n2 = mid.split("/")
        value = float(n1)/float(n2)
    before,after =re.split("\d+\.*\d*[\*\/]+[\+\-]?\d+\.*\d*",expr,1) #以第一个符合要求的字符串作为分隔符，第三个参数1代表第一个
    # print(before)
    # print(nn)  #报错，这里拆分成3部分，会出现ValueError: not enough values to unpack (expected 3, got 2)
    # print(mid)
    #拼接新的前中后3部分
    new_expr = "%s%s%s" % (before,value,after)
    # print(new_expr) #1+1.5/3*4  1+0.5*4  1+2.0
    #递归调用自己
    # my_list.append(new_expr)  #将每次产生的新表达式依次提交到列表，最后一个元素就是加减函数需要用到的表达式--参数
    # print(my_list)
    # print(my_list[-1])
    expr_list[0] = new_expr  #71，113行
    # chengchu(expr_list)
    # return my_list[-1]
    return chengchu(expr_list) #退出递归的时候，接受最后去掉乘除符号的表达式，依次传给它的上一层调用，最后返回去掉乘除的表达式
#给计算函数的264行，加减函数的参数就是这个去掉乘除符号的表达式

def add_sub(expr_list):#参数：列表（表达式作为列表的第一个参数）
    while True:  #替换++  --  +- -+等连续的符号
        # if "++" in expr_list[0] or "--" in expr_list[0] or "+-" in expr_list[0] or "-+" in expr_list[0]:
        if expr_list[0].__contains__('+-') or expr_list[0].__contains__("++") or expr_list[0].__contains__('-+') \
                or expr_list[0].__contains__("--"):
            expr_list[0] = expr_list[0].replace("+-","-")
            expr_list[0] = expr_list[0].replace("++","+")
            expr_list[0] = expr_list[0].replace("-+","-")
            expr_list[0] = expr_list[0].replace("--","+")
        else:
            break #替换完毕后，退出循环
    if expr_list[0].startswith("-"): #将数字最开始的负号提取出来  --- 相当于- ----相当于+
        expr_list[1]+=1 #每提取一次负号，自增1，奇数个负号就是负数，偶数个负号就是正数
        expr_list[0] = expr_list[0].replace("-","&")
        expr_list[0] = expr_list[0].replace("+","-")
        expr_list[0] = expr_list[0].replace("&","+")
        expr_list[0] = expr_list[0][1:]
    expr = expr_list[0]  #列表的第一个元素是待计算的表达式
    mch = re.search("[\-]?\d+\.*\d*[\+\-]{1}\d+\.*\d*",expr)  #90.1+90.2  90.1-90.2  匹配2个数相加减的情况
    # print(mch)
    if not mch: #递归出口，最后没有加减符号的时候，返回None
        return expr_list
    mid = re.search("[\-]?\d+\.*\d*[\+\-]{1}\d+\.*\d*",expr).group() #匹配加减法的2个数,左边第一个满足要求的
    # print(mid)
    #计算mid
    if len(mid.split("+"))>1:
        n1,n2 = mid.split("+")
        value = float(n1)+float(n2)  #将字符串转换成float进行计算
    else:
        n1,n2 = mid.split("-",2)
        value = float(n1)-float(n2)
    before,after =re.split("[\-]?\d+\.*\d*[\+\-]{1}\d+\.*\d*",expr,1) #以第一个符合要求的字符串作为分隔符，第三个参数1代表第一个
    # print(mid)
    # print(before)
    # print(after)
    #拼接新的前中后3部分
    new_expr = "%s%s%s" % (before,value,after)
    # print(new_expr) #1+1.5/3*4  1+0.5*4  1+2.0
    #递归调用自己
    expr_list[0] = new_expr  #将新表达式赋值给列表的第一个元素  671.113行
    # add_sub(expr_list)  #递归调用自己，参数是列表
    return add_sub(expr_list)

def compute(expr): #参数：表达式  计算函数 括号里面的值传入
    # print(expr)
    expr_list = [expr,0] #关键点：乘除法计算完毕后，递归返回的是None，如何将乘除法计算后的值，传给加减法（解决办法：将表达式作为列表的第一个元素传入）
    # print(expr_list)
    chengchu(expr_list)  #调用乘除函数，参数是列表，列表的第一个元素是待计算的表达式
    # print(chengchu(expr_list))  #乘除函数执行完毕后，return的是expr_list列表--72行（此列表的第一个元素就是没有乘除号的表达式）
    add_sub(expr_list)   #调用加减函数，参数是列表（此列表是261行的返回值），列表的第一个元素是待计算的表达式
    # print(add_sub(expr_list))
    if divmod(expr_list[1],2)[1] ==1:  #除以2的余数是1的话，代表是奇数，取负数
        result = float(expr_list[0])
        result = result * -1  #奇数个负号，取负数
    else:
        result = float(expr_list[0]) #偶数个符号，取整数  71行 113行 124行
        #关键点，这里如果不用列表的形式，直接表达式的话，会出现 ValueError: could not convert string to float:
        #如果是字典的第一个元素的话，前面的乘除法，修改了字典的第一个元素的值，变成了只含有加减号的表达式，在加减法函数，
        #接受的就是指含有加减号的，计算完毕后，字典的第一个元素的值变成了一个字符串，转换成float后，就正确了
    return result  #必须返回的是result，返回值是列表的第一个元素（待计算的表达式计算后，转换成float类型）

# @login  #相当于  qukuohao = login(qukuohao)  qukuohao=inner
def qukuohao(expr): #参数：表达式  取括号函数
    # mch = re.search("\(([\+\-\*\/]*\d+\.*\d*){2,}\)",expr)  #(-90.1*90.2+90.3)
    mch = re.search("\([^\(\)]+\)",expr)  #(-90.1*90.2+90.3)  #[^\(\)]  正则中中括号的用法
    # print(mch)  #匹配小括号开头，小括号结尾，中间不包含小括号的字符串  上述161 和162行都可以匹配小括号
    if not mch: #递归出口，最后没有小括号的时候，直接调用compute方法计算
        final = compute(expr)
        return final
    #匹配小括号开头，小括号结尾，中间不包含小括号，只包含数字或者加减乘除运算符,找出左边第一个符合要求的
    # mid = re.search("\(([\*\/\+\-]*\d+\.*\d*){2,}\)",expr).group()
    mid = re.search("\([^\(\)]+\)",expr).group()
    # print(mid)  #(-40/5)
    before,nothing,after =re.split("\(([\*\/\+\-]*\d+\.*\d*){2,}\)",expr,1) #以第一个符合要求的字符串作为分隔符，第三个参数1代表第一个
    # print(before)  #1-2*((60-30+
    # print(nothing)  #/5   这个值没用，split拆分成3部分和拆分成2部分的区别，这里拆分2部分报错 ValueError: too many values to unpack (expected 2)
    # print(after)   #*(9-2*5/3+7/3*99/4*2998+10*568/14))-(-4*3)/(16-3*2))
    #计算mid
    # print('before：',expression)
    mid = mid[1:len(mid)-1] #-8.0  切片去掉2端的小括号
    # print(mid)
    value = compute(mid)  #(-8.0)  调用计算函数，计算mid中值
    # print(type(mid))
    #拼接新的前中后3部分
    # print('%s=%s' %( mid, value))
    expr = "%s%s%s" % (before,value,after)
    # print(expr) #1+1.5/3*4  1+0.5*4  1+2.0
    #递归调用自己
    # print('after：',expression)
    # print("="*10,'上一次计算结束',"="*10)
    # print(qukuohao(expr))
    return qukuohao(expr)

if __name__ == "__main__":
    # expression = "1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )"
    # expression = "1-2*-30/-12*(-20+(400/2)*-3/-200*-(400-100)-(400-300))"
    @Filter(Login, Errorhandle)
    def main1():
        print("欢迎使用计算器，该计算器支持加减乘除四则元素，支持小括号优先级处理")
        while True:
            expression = input("请输入你要计算的表达式:") #待输入的字符串 1-2*-30/-12*(-20+(400/2)*-3/-200*-(400-100)-(400-300))
            expression = re.sub("\s*","",expression)  #去空格
            if not re.search("[a-zA-Z\!\@\#\$\\%\^\&\{\}\[\]\:\"\;\'\?\<\>]",expression):#计算表达式不能有大小写字母或者特殊字符
            # if not re.search("[a-zA-Z]",expression):#计算表达式不能有大小写字母和特殊字符
            #     print(re.search("[a-zA-Z]",expression))
                print("表达式计算结果是:",qukuohao(expression)) #调用去括号函数,并且打印该函数的返回值(不能只调用，不打印，否则少一步)
                print("表达式验证结果是: %s eval主要用于验证计算的结果是否正确" % eval(expression)) #验证计算器计算的最后值是否正确
                break
            else:
                print("\033[31;1m您输入的字符非法，无法计算，表达式不能含有大小写字母或者特殊字符\033[31;1m")
            # compute(expression)
            # print(eval("1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )"))
            # print(eval("1-2*-30/-12*(-20+(400/2)*-3/-200*-(400-100)-(400-300))"))
                # print(eval("1-2*-30/-12*(-20+(-2-2-400/2)*-3/-200*-(400-100)-(400-300))"))
    main1()


# re模块用于对python的正则表达式的操作。
#
# 字符：#
# 　　. 匹配除换行符以外的任意字符
# 　　\w	匹配字母或数字或下划线或汉字
# 　　\s	匹配任意的空白符
# 　　\d	匹配数字
# 　　\b	匹配单词的开始或结束
# 　　^	匹配字符串的开始
# 　　$	匹配字符串的结束
#
# 次数：#
# 　　* 重复零次或更多次
# 　　+	重复一次或更多次
# 　　?	重复零次或一次
# 　　{n}	重复n次
# 　　{n,}	重复n次或更多次
# 　　{n,m}	重复n到m次

# 正则表达式常用6种操作
# match 从头匹配
# search 匹配左边第一个满足要求的
# findall 匹配所有满足要求的存到列表
# sub 替换，最后一个参数可以指定最大替换次数，不写的话，默认全部替换，
#     写1的话，以左边第一个符合要求的字符串作为被替换对象
# split 拆分，最后一个参数可以指定最大替换次数，不写的话，默认全部替换，
#      写1的话，以左边第一个符合要求的字符串作为分隔符






