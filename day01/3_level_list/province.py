#！/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
#将文件转换成字典信息
def get_dict(info):
    with open(info,'r',encoding='utf8') as f:
        dict={}
        for line in f:
            new_line=line.strip().split()
            province=new_line[0]
            city=new_line[1]
            county=new_line[2]
            if province in dict:
                if city in dict[province]:
                    dict[province][city].append(county)
                else:
                    dict[province][city]=[]
                    dict[province][city].append(county)
            else:
                dict[province]={}
                dict[province][city]=[]
                dict[province][city].append(county)
    return dict

#获取各级信息列表函数
def get_num_list(dict):
    n=1
    num_dict={}
    for province in  dict.keys():
        num_dict[n]=province
        n += 1
    return num_dict

#测试输入是否为数字
def test_input(test):
    try:
        int(test)
    except ValueError:
        return 1

def main():
    entire_dict=get_dict('china.txt')
    #获取省级列表字典
    province_num_list=get_num_list(entire_dict)
    #省级列表循环
    while True:
        #设置标记位，为了跳出多级菜单
        flag='false'
        #打印省级列表信息
        for k,v in province_num_list.items():
            print(k,v)
        input_num=input('请输入对应省份的编号,退出输入q:').strip()
        if input_num == 'q':
            print('退出了！！！！')
            sys.exit(0)
        elif test_input(input_num)==1:
            print('您输入的不是数字！！！')
        elif int(input_num) not in province_num_list:
            print('输入编号不在列表范围内！！！')
        else:
            #编号对应的省份：
            p_name=province_num_list[int(input_num)]
            #获取市级列表dict
            city_num_list=get_num_list(entire_dict[p_name])
            #进入市级列表循环
            while flag=='false':
                for n,m in city_num_list.items():
                    print(n,m)
                input_city_num=input('请输入对应城市的编号,输入b返回上级菜单，输入q退出:').strip()
                #打印市级列表信息
                if input_city_num=='q':
                    print('退出了！！！')
                    sys.exit(0)
                elif input_city_num == 'b':
                    break
                elif test_input(input_city_num)==1:
                    print('您输入的不是数字！！！')
                elif int(input_city_num) not in city_num_list:
                    print('输入编号不在列表范围内！！！')
                else:
                    #标号对应的城市名称
                    city_name=city_num_list[int(input_city_num)]
                    #获取县级城市list
                    county_list=entire_dict[p_name][city_name]
                    while flag=='false':
                        a = 1
                        #打印县级列表信息
                        for i in county_list:
                            print(a,i)
                            a +=1
                        input_cent=input('请输入b返回上级菜单，输入q退出，输入s返回省级菜单：').strip()
                        if input_cent =='b':
                            break
                        elif input_cent=='q':
                            print('退出了！！！')
                            sys.exit(0)
                        elif input_cent=='s':
                            flag='true'
                        else:
                            if input_cent not in ['b','s','q']:
                                print('请按提示输入，谢谢！！！')

if __name__ == '__main__':
    main()