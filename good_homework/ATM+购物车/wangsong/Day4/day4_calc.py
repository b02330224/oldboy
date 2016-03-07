#!/usr/bin/env python
"""
__author__: super
blog : http://blog.csdn.net/songfreeman
this program return  a float value. run in 3.x
"""
import re


# 格式化字符串
def format_string(string):
    string = string.replace("--", "+")
    string = string.replace("-+", "-")
    string = string.replace("++", "+")
    string = string.replace("+-", "-")
    string = string.replace("*+", "*")
    string = string.replace("/+", "/")
    string = string.replace(' ', '')
    return string


# 检查表达式合法性
def check_expression(string):
    check_result = True
    # 括号是否匹配
    if not string.count("(") == string.count(")"):
        print("表达式错误,括号未闭合!")
        check_result = False
    if re.findall('[a-z]+', string.lower()):
        print("表达式错误,包含非法字符!")
        check_result = False
    return check_result


# 计算乘 、除法
def calc_mul_div(string):
    # 从字符串中获取一个乘法或除法的表达式
    regular = "\d+\.{0,}\d{0,}[\*\/][\-]{0,}\d+\.{0,}\d{0,}"
    # 如果还能找到乘或除法表达式
    while re.findall(regular, string):
        # 获取表达式
        expression = re.search(regular, string).group()

        # 如果是乘法
        if expression.count("*"):
            # 获取要计算的两个数
            x, y = expression.split("*")
            # 计算结果
            mul_result = str(float(x) * float(y))
            # 将计算的表达式替换为计算结果值
            string = string.replace(expression, mul_result)
            # 格式化一下
            string = format_string(string)

        # 如果是除法
        if expression.count("/"):
            # 获取要计算的两个数
            x, y = expression.split("/")
            # 计算除法
            div_result = str(float(x) / float(y))
            # 用结果替换表达式
            string = string.replace(expression, div_result)
            string = format_string(string)
    return string


# 计算加、减法
def calc_add_sub(string):
    # 定义正则表达式
    add_regular = "[\-]{0,}\d+\.{0,}\d{0,}\+[\-]{0,}\d+\.{0,}\d{0,}"
    sub_regular = "[\-]{0,}\d+\.{0,}\d{0,}\-[\-]{0,}\d+\.{0,}\d{0,}"

    # 开始加法
    while re.findall(add_regular, string):
        # 把所有的加法都算完,获取所有加法表达式
        add_list = re.findall(add_regular, string)
        for add_str in add_list:
            # 获取两个加法的数
            x, y = add_str.split("+")
            add_result = "+" + str(float(x) + float(y))
            string = string.replace(add_str, add_result)
        string = format_string(string)

    # 开始减法
    while re.findall(sub_regular, string):
        sub_list = re.findall(sub_regular, string)
        for sub_str in sub_list:
            numbers = sub_str.split("-")
            # -3-5的情况split会返回3个值
            if len(numbers) == 3:
                result = 0
                for v in numbers:
                    if v:
                        result -= float(v)
            else:
                x, y = numbers
                result = float(x) - float(y)
            # 替换字符串
            string = string.replace(sub_str, "+" + str(result))
        string = format_string(string)
    return string


if __name__ == "__main__":
    source = "1 - 2 * ( (60-30 +(-9-2-5-2*3-5/3-40*4/2-3/5+6*3) * (-9-2-5-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )"

    if check_expression(source):
        print("source: ", source)
        print("eval result: ", eval(source))

        while source.count("(") > 0:
            # 格式化
            source = format_string(source)
            # 去括号,得到括号的字符串,结果如:(30+6/3)
            strs = re.search('\(([/-]*\d+\.*\d*[\+\-\*/]+)+\d+\.*\d*\)', source).group()
            # 将括号的表达式进行乘、除运算
            replace_str = calc_mul_div(strs)
            # 将运算的结果在进行加、减运算
            replace_str = calc_add_sub(replace_str)
            # 将括号的字符串替换为计算结果,结果包含(),替换时去掉():[1:-1]
            source = format_string(source.replace(strs, replace_str[1:-1]))

        else:
            # 没有括号就到最后单一表达式了
            replace_str = calc_mul_div(source)
            # 算乘除
            replace_str = calc_add_sub(replace_str)
            # 算加减
            source = source.replace(source, replace_str)
        print("my result: ", source.replace("+", ""))