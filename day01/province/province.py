#！/usr/bin/env python
# -*- coding:utf-8 -*-
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
def get_province(f):
    n=1
    global province_num_dict
    for province in  f.keys():
        print(n,province)
        province_num_dict={}
        province_num_dict[n]=province
        n += 1
    return province_num_dict
def get_city(p):
    m = 1
    for city in p.keys:
        print(m,city)
        city_dict={}
        city_dict[m]=city
        m +=1
    return city_dict

def main():
    entire_dict=get_dict('china.txt')
    get_province(entire_dict)
    pro=input('选择省份对应的编号')
    print(entire_dict[province_num_dict[pro]].keys)

if __name__ == '__main__':
    main()