### CentOS7搭建LAMP

1. 安装Apache

   ```shell
   yum install httpd
   ```

   开启Apache

   ```shell
   systemctl install httpd
   ```

   浏览器测试

   ```http://192.168.3.4```

   ![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220607090116.png)

2. 安装PHP

   ```shell
   yum -y install php
   ```

   重启httpd

   ```shell
   systemctl restart httpd
   ```

   网站跟目录下新建php测试文件

   `/var/www/html/test.php`

   ```php
   <?php phpinfo(); ?>
   ```

   浏览器浏览`http://192.168.3.4/test.php`

   ![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220607090600.png)

3. 安装mariadb

   ```shell
   yum -y install mariadb-server
   ```

   启动mariadb

   ```shell
   systemctl start mariadb
   ```

   设置账户密码

   ```shell
   mysql_secure_installation
   ```

   进入mariadb测试

   ```shell
   mysql -u root -p
   ```

4. 将MySQL与数据库关联起来

   ```shell
   yum -y install php-mysql
   ```

5. 安装常用的php模块

   ```shell
   yum -y install php-gd php-ldap php-odbc php-pear php-xml php-xmlrpc php-mbstring php-snmp php-soap curl curl-devel
   ```

6. 重启Apache服务

   搭建完成！