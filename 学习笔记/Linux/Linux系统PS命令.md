## Linux系统命令

### PS

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

* R(TASK_RUNNING)

  正在运行或在队列中等待的状态

* S(TASK_INTERRUPTIBLE)

  可中断的睡眠状态，进程正在等待某个事件的发生被挂起

* D(TASK_UNINTERRUPTIBLE)

  不可中断的睡眠状态，不可中断指的并不是CPU不响应外部硬件的中断，而是进程不响应异步信号

* T(TASK_STOPPED or TASK_TRACED)

  暂停或跟踪状态

* Z(TASK_DEAD-EXIT_ZOMBIE)

  推出状态，进程成为僵尸进程，退出过程中，进程占有的所有资源将被回收

* W

  没有足够的分页可以分配

* <

  高优先级

* N

  低优先级



ps命令的用法：

* -e,-A显示所有进程
* -f 显示完整格式输出
* -a,所有进程,加上-x会显示没有控制终端的进程
* -u 显示指定用户的进程 如 ```ps -u```



### dpkg

* -s：查看安装包的信息（是否已经安装）



### 查看内核版本

more /ect/os-release



### linux口令强化

```
/etc/login.defs
PASS_MAX_DAYS 60  # 设置密码最长使用天数
PASS_MIN_DAYS 2      # 设置密码最短使用天数

```

```
/etc/security/pwquality.comf
minlen = 9
minclass = 2 # 最少字符类数
maxrepeat = 2	# 最大连续相同字符的出现次数
lcredit = -1	# 最少包含一个小写字母
ucredit = -1	# 最少包含一个大写字母
dcredit = -1	# 最少包含一个数字
ocredit = -1	# 最少包含一个其他字符
```

