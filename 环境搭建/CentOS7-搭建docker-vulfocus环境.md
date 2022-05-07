---
title: CentOS7 搭建docker-vulfocus环境
date: 2021-12-29 16:01:39
updated: 2021-12-29 16:01:39
categories: 环境搭建
tags:漏洞
urlname:
keywords:漏洞
---

# CentOS7 搭建docker-vulfocus环境

<br>

### 1.修改镜像源

```bash
mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup   #备份源文件
wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo   #下载新的源（这里用的是阿里镜像） 
yum clean all   #清除缓存
yum makecache    #生成缓存
yum -y update
```

<br>

### 2.搭建docker环境

此处使用国内daocloud一键安装命令

```bash
curl -sSL https://get.daocloud.io/docker | sh
```

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20211224131750.png)

```bash
systemctl start docker  #启动docker
```

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20211224132054.png)

<br>

### 3.配置静态IP地址

网卡名：ens33

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20211224135544.png)

```bash
vi /etc/sysconfig/network-scripts/ifcfg-ens33  
```

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20211224140100.png)

```bash
service network restart  #重启network
```

此处要注意：要注意端口转发功能是否开启，没有开启的话执行下面指令开启

```bash
#我这里使用的是centos7
vi /etc/sysctl.conf
#新增一行
net.ipv4.ip_forward=1
#执行命令
systemctl network restart
#查看是否修改成功
sysctl net.ipv4.ip_forward
```

<br>

### 4.搭建vulfocus



```bas
docker pull vulfocus/vulfocus:latest   #拉取vulfocus镜像
```

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20211224135129.png)

```bas
docker miages   #查看镜像仓库
```

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20211224135157.png)

```bash
docker run -d -p 8081:80 -v /var/run/docker.sock:/var/run/docker.sock -e VUL_IP=192.168.2.101 8a99241c264f    # 8a99241c264f 为 IMAGE ID···
```

```bash
docker ps   #查看正在运行的容器
```

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20211224144945.png)

用浏览器访问就OK了！！（初始用户名密码为：admin-admin）



![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20211224145121.png)
