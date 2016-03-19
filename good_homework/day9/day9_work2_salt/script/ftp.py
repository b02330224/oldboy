#!/usr/bin/env python
import paramiko
import os
import sys
from multiprocessing import Pool
from module import parser
from conf import settings
from module.common import write_log

def run(*args):
    """
    执行ftp传文件功能
    :param args:
    :return:
    """
    # 进行操作的主机字典
    exec_hosts = {}
    # 获取要执行的package名称
    exec_group = args[0]
    package_name = args[2]
    # 加载 package 文件
    package_file = os.path.join(settings.package_path, "{name}.sls".format(name=package_name))
    # 判断执行package文件是否存在
    if not os.path.exists(package_file):
    	print("\n\033[31;1m package  '{0}' not found! \033[0m".format(package_name))
    	sys.exit(0)
    	
    # 加载文件信息
    sftp_data = parser.get_package_date(package_file)
    # 根据组获取组内的所有主机信息
    host_in_group = parser.search_host_by_group(exec_group)
    if len(host_in_group) == 0:
        print("\n\033[31;1m no groupname '{0}' found! \033[0m".format(exec_group))
        sys.exit(0)

    # 如果配置文件中指定hosts：all，对组中所有主机进行配置执行
    if sftp_data['hosts'] == 'all':
        for k, v in host_in_group.items():
            exec_hosts.update(parser.host_info_by_ip(k))

    else:
        # 如果是指定部分IP执行 ip1,ip2
        ip_list = sftp_data['hosts'].split(",")
        for ip in ip_list:
            exec_hosts.update(parser.host_info_by_ip(ip))

    runpackage(sftp_data, exec_hosts)


def runpackage(sftp_data, hosts):
    """
    根据指定的文件操作数据、操作主机进行处理，格式化数据，并开启线程调用上传模块进行上传
    :param sftp_data: 要处理的文件信息数据 字典
    :param hosts: 主机信息字典
    :return:
    """
    # 获取 sftp 的执行方式： put / get ,上传的源及目标文件
    sftp_method = sftp_data['exec_method'].split(".")[1]
    if sftp_method == "put":
        sftp_data_source = os.path.join(settings.BASE_DIR, sftp_data['source'])
        sftp_data_target = sftp_data['name']
        # check source file is exists
        if not os.path.exists(sftp_data_source):
            print("\n\033[31;1m no file '{0}' found! \033[0m".format(sftp_data_source))
            sys.exit(0)
    else:
        sftp_data_source = sftp_data['source']
        sftp_data_target = os.path.join(settings.BASE_DIR, sftp_data['name'])

    # 开启5个线程池,开始执行上传的操作
    pool = Pool(5)
    host_info = {}
    #print(hosts)
    for k, v in hosts.items():
        host_info.clear()
        host_info[k] = v
        pool.apply_async(_sftp_put, args=(sftp_data_source, sftp_data_target,sftp_method), kwds=host_info)

    pool.close()
    pool.join()


def _sftp_put(source, distinct, sftp_method,  **host):
    """
    执行文件传输，
    :param source:源文件
    :param distinct: 目标文件
    :param sftp_method: sftp方式 上传 put / 下载 get
    :param host: 远程访问的主机信息
    :return:
    """
    try:
        ip = list(host.keys())[0]
        host_item = host[ip]
        port = int(host_item["port"])
        user = host_item["user"]
        key = host_item["key"]

        #print(ip,port,user,key)
        transport = paramiko.Transport(ip, port)
        if host_item['auth_type'] == 1:
            transport.connect(username=user, password=key)
        else:
            pkey = paramiko.RSAKey.from_private_key_file(os.path.join(settings.RSAKEY, key))
            transport.connect(username=user, pkey=pkey)

        ssh_sftp = paramiko.SFTPClient.from_transport(transport)
        if sftp_method == "put":
            ssh_sftp.put(source, distinct)
            print("\033[1;31m\n local[ {0} ] >>>>> upload to >>>>>> {1}[ {2} ]   finished \033[0m".format(source, ip, distinct))
        else:
            #print(source, distinct)
            ssh_sftp.get(source, distinct)
            print("\033[1;34m\n local[ {0} ] <<<<<< download from <<<<<<< {1}[ {2} ]   finished \033[0m".format(distinct, ip, source))

        transport.close()
    except Exception as e:
        write_log(e, "error")