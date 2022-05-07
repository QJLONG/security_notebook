## phpweb代码审计练习（Fortify的使用）

<br>

### 实验环境

###### 系统：WIndows7

软件：phpstudy2018

​			Fortify、

<br>

### 实验目的

在已经搭建好的phpweb站点上练习使用源代码审计工具Fortify

<br>

### 实验过程

打开Fortify工具，加载phpweb站点源码

并开始扫描

![](https://s2.loli.net/2022/03/14/n6osYC2bfMdiX95.png)

扫描结果如下：

![](https://s2.loli.net/2022/03/14/RFiOaodjGutT6kg.png)

通过查看左侧目录可以发现该站点存在XSS，SQL注入等多个漏洞

先尝试着看一下SQL注入

```php
//淇敼绠＄悊鍛樺瘑鐮佸拰鐢ㄦ埛缁戝畾
		$admin_user=$_POST["admin_user"];
		$admin_pass=$_POST["admin_pass"];
		$dbhost=$_POST["dbhost"];
		$dbuser=$_POST["dbuser"];
		$dbpwd=$_POST["dbpwd"];
```

上述代码中，程序通过POST方式获取参数admin_user，这个参数是空的，Fortify提示我们在下面的代码中，程序将admin_user这一参数直接拼接到SQL语句中，从而形成了SQL注入漏洞。

```php
$connect = @mysql_connect($dbhost, $dbuser, $dbpwd); 
		if ($connect) {
			mysql_query("update ".$dbname.".".$tablepre."_base_admin set user='$admin_user',password='$mdpass'", $connect);
			mysql_query("update ".$dbname.".".$tablepre."_base_adminrights set user='$admin_user'", $connect);
			mysql_query("update ".$dbname.".".$tablepre."_base_config set `value`='$username' where `variable`='phpwebUser'", $connect);
			mysql_query("update ".$dbname.".".$tablepre."_base_config set `value`='$siteurl' where `variable`='SiteHttp'", $connect);
		}
```

在Fortify中，有一个Diagram模块，能够更直观地显示某个漏洞的产生原因，我们可以借此更方便地验证并利用该漏洞

![](https://s2.loli.net/2022/03/14/YixCqFV4W2youHQ.png)

该站点文件在/base/install/index.php

在phpweb安装说明中提示我们安装成功后删除base/install文件夹下的所有文件所以这个站点文件无法检测，进行下一个

<br>

再来尝试一个XSS

![](https://s2.loli.net/2022/03/14/nTvNzWlerYJtxf2.png)

advs/admin/link.php:151

```php
	echo "<script>self.location='link.php?groupid=".$groupid."'</script>";
```

该站点文件中，通过REQUEST方式获取参数groupid，并通过echo函数输出出来，因此形成了反射型xss漏洞

到该站点下测试一下

```http://127.0.0.1/phpweb/advs/admin/link.php?groupid='"><sCrIpT>alert(/hummer/)</sCrIpT>```

![](https://s2.loli.net/2022/03/14/3CjVTWuIU7gBkEh.png)

测试成功！！

<br>

