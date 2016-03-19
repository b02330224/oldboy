#!/usr/bin/env python
import os
import sys
import paramiko
from multiprocessing import Pool
from module  import parser
from conf import settings
from module.common import write_log


def run(*args):
    #print("args:", args)
    groups = args[0]
    cmd = args[2]
    # 对所有配置的服务器执行命令
    if groups == "*":
        hosts = parser.load_host_all()
    else:
        # 根据组名执行命令
        hosts = parser.search_host_by_group(groups)
    if len(hosts) == 0:
        print("\033[31;1m no group name ' {0} ' found \033[0M".format(groups))
        sys.exit(0)

    # 设置5个进程池
    pool = Pool(5)
    for ip in hosts.keys():
        host_info = parser.host_info_by_ip(ip)
        pool.apply_async(_ssh_exec_cmd, args=(cmd,), kwds=host_info)
    pool.close()
    pool.join()


def _ssh_exec_cmd(commandstr, **host):
    """
    paramiko 执行命令方法
    :param hostlist: 主机列表{ip:[{user: , key: , auth_type: }]}
    :param commandstr: 执行的命令
    :return:
    """
    ip = list(host.keys())[0]
    host_item = host[ip]
    port = int(host_item["port"])
    user = host_item["user"]
    key = host_item["key"]

    try:
        # 开始登录服务器并执行命令
        transport = paramiko.Transport(ip, port)
        if host_item["auth_type"] == 1:
            transport.connect(username=user, password=key)
        else:
            pkey = paramiko.RSAKey.from_private_key_file(os.path.join(settings.RSAKEY, "id_rsa"), password=key)
            transport.connect(username=user, pkey=pkey)

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh._transport = transport
        stdin, stdout, stderr = ssh.exec_command(command=commandstr)

        print("\033[1;31m IP -> {0} : \033[0m \n".format(ip))
        err_result = stderr.read().decode()
        out_result = stdout.read().decode()
        if len(err_result) > 0:
            print(err_result)
        if len(out_result) > 0:
            print(out_result)

        transport.close()
    except Exception as e:
        print(e)
        write_log(e, "error")
