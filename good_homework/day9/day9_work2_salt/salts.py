#!/usr/bin/python3.4

import sys

from module import common

if __name__ == "__main__":
    args = sys.argv[1:]
    #args = ['web_server', 'ftp.cuu', 'mysql']
    #print(args)
    try:
        exec_module = args[1]
        # 如果参数cmd.run语法错误，直接抛异常
        if exec_module.count(".") == 0:
            raise IndexError

        # 获取执行的模块名称cmd or ftp
        modulename = exec_module.split(".")[0]
        funcname = exec_module.split(".")[1]
        # 导入模块
        modobj = __import__("script.{0}".format(modulename))
        modobj = getattr(modobj,modulename)
        funcobj = getattr(modobj, funcname)
        funcobj(*args)
    except (ImportError,IndexError):
        common.write_log("Import module error", "error")
        print("\033[33;1m no module {0} found \033[0m".format(exec_module))
    except Exception as e:
        common.write_log(e, "error")
        print("\033[33;1m system run Error,check logs\033[0m")







