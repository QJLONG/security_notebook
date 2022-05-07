## 1、五个基本单位

### 数据库服务器  

用来运行数据库服务的一台电脑，可以放在多台电脑

### 数据库

一个数据库服务器里有多个数据库， 默认端口：3306

用户名：root

密码：root

localhost  ：127.0.0.1

### 数据表  

用于区分不同的数据：角色表、武器表、用户信息表等等

### 数据字段

也叫数据列，用户信息分为多个列：用户编号、哟呼ID、用户密码等等

### 数据行

行是真正的数据

## 2、Mysqul连接数据库

![image-20201026214937784](C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201026214937784.png)

## 3、Mysql数据库操作

基本语法：

数据库的导入与导出：

![image-20210105141832840](C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20210105141832840.png)

CREATE DATABASE 数据库名           创建数据库

show databases;          查看数据库 **注意databases是复数！！**

 use php;                         进入库     

show tables;                    查看类                             

drop database php;         删除库

create table emp（

ename varchar(10),   字符型

hiredate date,         日期型

sal float(10,2)       浮点型

);                                                         创建表

desc 表名        

<img src="C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201027213020050.png" alt="image-20201027213020050" style="zoom: 80%;" />

show create table emp \G;   查看如何编辑表

<img src="C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201027213256189.png" alt="image-20201027213256189" style="zoom:80%;" />

drop table emp;              删除表

修改表字段类型       alter table 表名 modify    前字段名   新字段名；

增加表字段           alter table 表名 add column  字段名 类型；

按顺序添加字段       alter table emp add qwe varchar(10) after sal;

删除字段                 alter table emp **drop column** qwe;

改字段名                  alter table emp **change** ename ename1 v**archar(10)**;

把某个字段调整顺序   alter table emp modify sal1 float(10,2) after ename;

把某个字段放在最前（后）面   alter table emp **modify** sal float(10,2) first;

改表名                   alter table emp rename biao;

## 4、数据类型

tinyint   1字节

smallint   2字节

medium   3字节

int        4字节

<img src="C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201030134536840.png" alt="image-20201030134536840" style="zoom:80%;" />



<img src="C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201030134639076.png" alt="image-20201030134639076" style="zoom:80%;" />

<img src="C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201030134752962.png" alt="image-20201030134752962" style="zoom:67%;" />

<img src="C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201030135043234.png" alt="image-20201030135043234" style="zoom:80%;" />

![image-20201030135519757](C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201030135519757.png)

## 5、索引

### 普通索引

alter table 表 add index(字段)

例：alter table emp add index (ename);

为 emp表的ename字段增加索引

### 唯一索引

alter table emp add unique(字段);

例：alter table emp add unique(ename);

为emp表中的ename字段增加索引

### 全文索引

alter table 表 add fulltext(字段)

例：alter table emp add fulltext(ename)

为emp表中的ename字段添加全文索引

## 6、增删改查

### 插入

```mys
insert into emp (ename,sal1) values('hzl,20')
insert into emp values('hzl',20);
```

### 基础查询

<img src="C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201031112649627.png" alt="image-20201031112649627" style="zoom:80%;" />

``` my
select *from money;
```

![image-20201031115228345](C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201031115228345.png)

### 指定字段查询

``` my
select age from money;
```

![image-20201031115718026](C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201031115718026.png)

查询不重复记录

``` my
select distinct age deptno from money;
```

条件查询

```my
 select * from money where age=21;
```



按照一定顺序查询

```my
select username,password,age,sex from money order by age desc;
```

其中  desc为降序；asc为升序

取前两名：

```my
select username,password,age,sex from money order by age desc limit 2;
```





## 7、函数

<img src="C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201108212602611.png" alt="image-20201108212602611" style="zoom:80%;" />

``` my
select count(age) from money;  #查询个数
```

```my
select count(age) as sum from money;   #查询个数后给个数命名
```



分组：

group by 

## 8、结果再过滤

having 与 where 具有相同的效果，后接条件

```my
select * from money having age=23;
```

## 9、联合表查询

``` my
 select u.uid,u.username,o.oid,o.uid,o.name from user u, order_goods o where u.uid = o.oid;
```

<img src="C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201113130222290.png" alt="image-20201113130222290" style="zoom:80%;" />



``` my
select * from user left join order_goods on user.uid = order_goods.uid;
```

<img src="C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201113130446564.png" alt="image-20201113130446564" style="zoom:80%;" />

```my
select * from user left join order_goods on user.uid = order_goods.uid;#左查询
```

<img src="C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201113130922403.png" alt="image-20201113130922403" style="zoom:80%;" />

```my
select * from user right join order_goods on user.uid = order_goods.uid;#右查询
```

<img src="C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201113131003396.png" alt="image-20201113131003396" style="zoom:80%;" />

``` my
select * from user where uid in (1,3,4);
```

<img src="C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201113131310448.png" alt="image-20201113131310448" style="zoom:80%;" />

``` my
select * from user where uid in(select uid from order_goods);#括号里可以放条件
```

<img src="C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201113131554116.png" alt="image-20201113131554116" style="zoom:80%;" />![image-20201113133150005](C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201113133150005.png)

``` my
 select uid from user union select name from order_goods;#联合查询，放在一起显示
```

<img src="C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201113132013863.png" alt="image-20201113132013863" style="zoom:80%;" />

``` my
 update money set  age=age+20 where uid = 1; # 更新表中的字段
```

<img src="C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201113133232047.png" alt="image-20201113133232047" style="zoom:80%;" />

``` my
select * from money; #删除记录
```

<img src="C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201113133555429.png" alt="image-20201113133555429" style="zoom:80%;" />

``` my
truncate money;  #清空表
```

<img src="C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20201113133811553.png" alt="image-20201113133811553" style="zoom:80%;" />

## 10、权限设置

权限提升：

updata staff set s_power=1 where s_user='staff_jack' 