### phpweb安装：

下载地址：

https://ahdx.down.chinaz.com/CMS%BD%A8%D5%BE/phpweb_base.zip

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220206132245.png)

下载完成后解压 ，将www目录重命名为phpweb，放进phpstudy网站根目录中后通过浏览器打开。

这里注意，phpweb的运行需要服务器安装Zend，phpstudy2018中只有5.2.x版本安装了Zend，所以浏览器打开后如果出现乱码，需要调整版本为5.2.x并重启修改php.ini配置文件，具体参考：

[(142条消息) phpweb安装出现乱码解决方案_小裁缝233的博客-CSDN博客_phpweb安装乱码](https://blog.csdn.net/qq_45001989/article/details/108184692)

打开如下图：

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220206131957.png)

点击接收协议后来到下图：

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220206132057.png)

这里提示我们需要称为会员才能继续进行安装操作,查看该页面的源代码尝试绕过：

phpweb/base/install/index.php:27

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220206141142.png)

```php
if ($_POST['nextstep'] == 1) {

			$c_params = array (
				'username' => $_POST['username'], 
				'password' => $_POST['password'],
				'domain' => $_SERVER['HTTP_HOST']
				);
			$ans = $customer -> call ("iChkUser", $c_params);
			if ($err=$customer->getError()) {
				$errinfo=$customer->response;
				$error_msg="<font style=\"color: red;\">无法连接到验证服务器，错误信息：".$errinfo."</font><br /><br />";
				$noinstall="<script>document.all['subm'].disabled = true;</script>";
				$donext=false;
			}elseif($ans==false || $ans==""){
					$error_msg = "<font style=\"color: red;\">无法连接到验证服务器，请检查是否已连接网络，或稍侯再试！</font>";
					$noinstall= "<script>document.all['subm'].disabled = true;</script>";
					$donext= false;
			}elseif($ans=="NOUSER") {
					$error_msg = "<font color='red'>会员登录账号或密码错误，请重新输入正确的登录帐号和密码</font><br /><br />";
					$donext= false;
			}elseif($ans!="OK") {
					$error_msg = "<font color='red'>身份验证未通过：".$ans."</font><br /><br />";
					$donext= false;
			}else{
				$donext=true;
			}
	}
```

这段代码的功能就是判断用户是否为会员，将该段代码删掉，替换为```$donext=true```;即可

保存刷新后，随便输入会员账号密码即可进入下一步。

来到第四步，需要对数据库相关信息进行配置：

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220206142413.png)

打开下载的安装说明：

```php
<?php

#[数据库参数]
$dbHost="localhost";            #数据库服务器名
$dbName="dbpw";                 #数据库名
$dbUser="root";                      #数据库用户名
$dbPass="mypassword";        #数据库密码 可以自定义我这里改成了root

#[数据表前缀]
$TablePre="dev";

#[语言]
$sLan="zh_cn";

#[网址]
$SiteUrl="http://www.mydomain.com/";                    #当前网址，很重要，末尾必须有"/"

#----------------------------------#


?>
```

将phpweb/base/install/inc.php中的相关信息替换掉

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220206144908.png)

创建数据库的过程中可能需要远程连接，phpstudy2018默认是不允许远程访问数据库的

结局方法如下：

```
1、先在服务器中通过命令行方式（打开phpstudy界面->右下角其他菜单选项->MySQL工具->MySQL命令行）

登录mysql：mysql   -u root -p 密码 （如果mysql初始账号和密码都是root）

2、执行use mysql; 

3、执行grant all privileges on *.* to 
root@'%' identified by '密码'; 

4、执行flush privileges;
```

修改配置文件后在浏览器继续第四步安装

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220206144448.png)

创建完成后一路下一步并设置密码即可



登录后台如下：

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220206145040.png)

<br>





