#!/usr/bin/env python
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# 日志记录文件
SYSLOG_FILE = os.path.join(BASE_DIR, "logs/syslog.log")
OPLOG_FILE = os.path.join(BASE_DIR, "logs/oplog.log")
# 日志输出级别 info,debug,error,warning
LOG_LEVEL = "info"
LOG_PRING = False

# 配置文件 package 包存放目录,用来存放执行命令的 yaml文件
package_path = os.path.join(BASE_DIR, "package")

# 主机配置文件
hosts_config = os.path.join(BASE_DIR, "conf/hosts.yaml")
# paramiko 密钥登录时密钥路径
RSAKEY = os.path.join(BASE_DIR, "sshkey")
