#!/usr/bin/env python
import logging
from conf import settings

def get_log_level():
    level = settings.LOG_LEVEL
    result = logging.INFO
    if level == "debug":
        result = logging.DEBUG
    if level == "warning":
        result = logging.WARNING
    if level == "error":
        result = logging.ERROR
    return result


def write_log(msg, msgtype, log_type="sys"):
    log = logging.getLogger("SSHLOG")
    log.setLevel(get_log_level())

    log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # 记录到文件
    if log_type == "sys":
        filehandle = logging.FileHandler(settings.SYSLOG_FILE)
    else:
        filehandle = logging.FileHandler(settings.OPLOG_FILE)
    filehandle.setLevel(logging.INFO)
    log.addHandler(filehandle)
    filehandle.setFormatter(log_format)

    # 打印屏幕,只打印错误日志
    if settings.LOG_PRING:
        screenhandle = logging.StreamHandler()
        screenhandle.setLevel(logging.INFO)
        log.addHandler(screenhandle)
        screenhandle.setFormatter(log_format)

    if msgtype == "info":
        log.info(msg)
    if msgtype == "error":
        log.error(msg)
    if msgtype == "debug":
        log.debug(msg)

    log.removeHandler(filehandle)
    if settings.LOG_PRING:
        log.removeHandler(screenhandle)