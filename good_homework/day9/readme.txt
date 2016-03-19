day9包括两个文件：

day9_work1_select.py
程序说明：
    select 的socketserver端详细解释说明文件。


day9_wrok2_salt
程序功能：
    模拟saltstack功能远程执行 命令并返回结果、 远程执行文件上传、下载

程序执行命令：
1： 远程执行命令
    salts.py  web_server cmd.run "df -hl"
    args:
        web_server   服务器所属组, 对所有服务器进行命令使用  \*
        cmd.run       执行cmd命令模块
2:  远程执行文件上传、下载
    salts.py  web_server  ftp.run httpd
    args:
         web_server    服务器所属组
         ftp.run          执行的ftp模块
         httpd            package名
         
程序目录结构：
ay9_work2_salt/
├── conf                                 配置目录
│   ├── hosts.yaml                      主机配置文件信息
│   └── settings.py                      系统配置文件
├── file_source                       上传下载文件目录
│   ├── httpd.conf                      
│   └── my.cnf
├── logs                                 系统日志目录
│   └── syslog.log                        系统日志
├── module                            模块目录
│   ├── common.py                     公共模块
│   └── parser.py                          ymal文件处理模块
├── package                          上传下载配置包目录
│   ├── httpd.sls                           
│   └── mysql.sls
├── salts.py                            系统主程序文件
├── script                               命令处理模块目录
│   ├── cmd.py                            执行命令模块   cmd.run
│   └── ftp.py                              文件传送 模块  ftp.run
├── sshkey                             密钥存放目录
    ├── id_rsa
    └── id_rsa.pub
