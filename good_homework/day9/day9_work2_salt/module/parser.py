#!/usr/bin/env python
import yaml
from conf import settings

hostconfig = settings.hosts_config


def host_info_by_ip(ip):
    """
    根据 IP 地址获取该ip对一个的服务器信息，返回一个字典
    :param ip: ip地址
    :return: 信息字典{ip:{user:'test',auth_type：1}}
    """
    return_dict = {}
    with open(hostconfig, 'r') as f:
        hosts_dict = yaml.load(f)
        host = hosts_dict[ip]
        for item in host:
            for k, v in item.items():
                return_dict[k] = v
    return {ip: return_dict}


def search_host_by_group(groupname):
    """
    从服务器信息文件hosts.yaml中读取指定组的主机信息
    :param groupname: 组名称
    :return: 返回服务器信息字典{ip:[{'user':'test'},{'key':'124'}]}
    """
    return_dict = {}
    tmp_dict = {}
    with open(hostconfig, 'r') as f:
        hosts_dict = yaml.load(f)
        for ip, host_info in hosts_dict.items():
            for item in host_info:
                for k, v in item.items():
                    tmp_dict[k] = v
                    if k == "group" and v == groupname:
                        return_dict[ip] = host_info
    return return_dict


def load_host_all():
    """
    从服务器信息文件hosts.yaml中读取所有的主机信息
    :return: 服务器信息字典
    """
    with open(hostconfig, 'r') as f:
        return yaml.load(f)


def get_package_date(package_file):
    """
    执行ftp操作，从package文件读取信息，返回字典数据
    :param package_file: 处理文件
    :return: 字典信息
    """
    data_dict = {}
    with open(package_file, 'r') as f:
        data = yaml.load(f)
    data_dict['exec_method'] = list(data.keys())[0]
    for method, data_info in data.items():
        for item in data_info:
            for k, v in item.items():
                data_dict[k] = v

    return data_dict
