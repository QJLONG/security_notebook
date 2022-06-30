### Linux系统常用命令

#### 查看发行版本

```shell
cat /etc/*-release
```



#### ls

```shell
man  ls		#输出ls命令的官方文档
ls -a		#显示隐藏文件 
ls -t  		#最近修改过的在最上
ls -l		#列出详细信息
ls -r		#逆序排列
ls -u		#访问时间
```

#### chmod

u(User) 	

g(Group)	

o(Other)
r=4	w=2	x=1

```shell
chmod u+x g+w hello,sh
chmod u=rwx,g=rw,o=r hello.sh
chmod a+x
chmod 746
```

#### find

```shell
find / -name "*.txt" -o -name "*.pdf"		#联合查询 -o=or
find / ! -name "*.txt" 
find . -type f 时间戳
               -atime -amin 访问时间
               -mtime -mmin 修改时间
               -ctime -cmin 比mtime多了修改权限
find . -type f -atime -7 	#七天内/7 恰好七天前/ +7超过7天未访问
find . -type f -perm 777 	#权限查找
find . -type f -name "*.txt" ! -perm 777
find . -type  f -user root
```

#### cat

```shell
cat 1.txt 2.txt> 3.txt		# 将1.txt和2.txt合并到3.txt中
```

#### more

按页显示 空格下一页  b上一页

```shell
more +3 test.txt		# 从第三行起显示
more -5 test.txt		# 每屏显示5行
```

#### less

与more相似 可以显示行号

```shell
less -N /etc/passwd		# 显示行号
```

#### vi

```shell
Ctrl+f 		# 向下翻页
Ctrl+b		# 向上翻页 
:行号
```

#### sed

修改后输出  但不保存

```shell
sed ‘s/1/2' 1.txt		# 将1.txt文件中的1替换为2
```

#### grep

正则表达式搜索

``` 
grep "" filename
```

#### mkdir

```shell
mkdir -pm 700 /tmp/eshare/破军
```

#### rm

#### tar

```shell
tar -zxvf filename	# 解压
tar -zcvf filename	# 压缩
```

#### stat

输出文件信息

```shell
stat 1.txt
```

#### last

日志存放路径 /var/log

```shell
last		# 查看登录主机的用户的信息
lastb		# 查看登录错误用户的信息
```

#### w

查看已经登录的用户的列表

#### ps

```shell
ps -aux
```

#### pidof

用进程名称查找指定进程的进程号

#### lsof

查看进程与文件

```shell
lsof filenaem	# 显示打开文件的进程
lsof -i :22		# 查看端口运行情况
lsof -p PID		# 列出进程打开的文件
```

#### mpstat

显示各个可用CPU状态信息

#### top

#### netstat

```shell
netstat -an | grep ':80'
```

#### sort

排序

#### PS

-aux：显示所有包含其他使用者的进程

输出格式：

user	pid	%cpu	%mem	vsz	rss	tty	stat	start time	command

user:进程拥有者

mem:占用的记忆体使用率

stat:进程的状态

start:进程开始时间

time:执行的事件

command:执行的命令

状态：

- R(TASK_RUNNING)

  正在运行或在队列中等待的状态

- S(TASK_INTERRUPTIBLE)

  可中断的睡眠状态，进程正在等待某个事件的发生被挂起

- D(TASK_UNINTERRUPTIBLE)

  不可中断的睡眠状态，不可中断指的并不是CPU不响应外部硬件的中断，而是进程不响应异步信号

- T(TASK_STOPPED or TASK_TRACED)

  暂停或跟踪状态

- Z(TASK_DEAD-EXIT_ZOMBIE)

  推出状态，进程成为僵尸进程，退出过程中，进程占有的所有资源将被回收

- W

  没有足够的分页可以分配

- <

  高优先级

- N

  低优先级



ps命令的用法：

- -e,-A显示所有进程
- -f 显示完整格式输出
- -a,所有进程,加上-x会显示没有控制终端的进程
- -u 显示指定用户的进程 如 `ps -u`

#### dpkg

- -s：查看安装包的信息（是否已经安装）

### rpm -qa

列出所有安装过的包

#### 查看内核版本

more /ect/os-release

#### linux口令强化

```
/etc/login.defs
PASS_MAX_DAYS 60  # 设置密码最长使用天数
PASS_MIN_DAYS 2      # 设置密码最短使用天数

/etc/security/pwquality.comf
minlen = 9
minclass = 2 # 最少字符类数
maxrepeat = 2   # 最大连续相同字符的出现次数
lcredit = -1    # 最少包含一个小写字母
ucredit = -1    # 最少包含一个大写字母
dcredit = -1    # 最少包含一个数字
ocredit = -1    # 最少包含一个其他字符
```

### 密码复杂度设置（ubuntu）

安装PAM的cracklib模块,cracklib能提供额外的密码检查能力

sudo apt-get install libpam-cracklib

修改配置文件对新密码进行限制

* 禁止使用旧密码

  添加remember=5，表示禁止使用最近使用过的5个密码

  ![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220516103822.png)

* 设置密码最短长度

  将minlen的值修改为10，表示密码长度最少为10

  ![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220516105014.png)



#### 组合

![](https://s2.loli.net/2022/02/18/P1fFGo6N4EUji2u.png)

![](https://s2.loli.net/2022/02/18/pTcP4bUqBIZdVeF.png)

### Windows系统常用命令

#### net user

```shell
net user name pwd /add /expires:never
net user name /delete
net user name newpwd		# 修改用户密码
net user name /active:yes	# 激活用户
图形界面：计算机管理->用户->属性->禁用
```

#### net localgroup

```shell
net localgroup Administrators name /add		# 加入管理员组
net localgroup Administrators name /delete
```

#### dir

```shell
dir /a:h /s 显示本目录及其子目录隐藏文件
```

#### echo

```shell
echo "test test" > 1.txt		# 覆盖
echo "tesr" >> 1.txt			# 追加
```

#### del

```shell
del name		# 删除文件
```

#### rd

```shell
rd folderName /S /Q		# 删除目录
rd folderName 			# 删除空目录
```

#### type fineName 

查看文件内容

#### ren

重命名

```shell
ren fine1 fien2
```

#### attrib

```shell
attrib +S +H filename  # 添加隐藏属性的文件
```

#### find

``` shell
find "abc" 1.txt	# 查找abc所在的行并输出该行
find /n "abc" 1.txt	# 同时输出行号
```

#### natstat

``` shell
netstat -ano	# 列出所有端口的使用情况
```

#### tracert

```shell
tracert ip		# 跟踪路由
```

#### nslookup

```shell
nslookup www.baidu.com	# 查看指定域名的dns信息
```

#### route

打印路由表

#### net

```shell
net view 	# 查看当前局域网其他连接着
net start	# 查看开启哪些服务
net start 服务名	# 开启一个服务
net use K: \\ip\C$	# 将服务器的C盘映射成K盘
net share # 查看本地开启的共享
```

### Linux服务

系统服务

网络服务

独立服务

临时服务

超级服务xinetd

Linux 网络服务定义文件：

**```/etc/services```**

#### 常见的守护进程

crond  :  linux下的计划任务

#### 文件系统

普通文件：文本文件、二进制文件

目录文件

设备文件：常在```**/dev**```目录下

/var/log/secure

lastlog

查看系统中所有用户最后一次登录信息



### Linux系统权限

普通用户UID500-6000

用户配置文件

/etc/passwoed

/etc/shadow

密码存储格式：

![](https://s2.loli.net/2022/02/18/Tqbi5dFVQGt4Uwj.png)

#### 创建用户

useradd name

passwd username 设置密码

userdel name

usermode -L name

usermode -U name

gpasswd -a Uname Gname

gpasswd -d Uname Gname

### Windows系统权限

whoami /user 查看标识符

隐藏账户无法通过netuser查看

net user test1$ test

ca