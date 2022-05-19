## linux软件包

Linux下的软件包分为两种，分别是**源码包**和**二进制包**

二进制包是源码包经过编译之后的安装报，安装速度相对于源码包更快。

### 两大主流二进制包管理系统：

* RPM包管理系统：功能强大，安装、升级、査询和卸载非常简单方便，因此很多Linux发行版都默认使用此机制作为软件安装的管理方式，例如Fedora、CentOS、SuSE等

* DPKG包管理系统：由Debian Linux所开发的包管理机制，通过DPKG包，Debian Linux就可以进行软件包管理，主要应用在Debian和Ubuntu中。



源码包一般包含多个文件，为了方便发布，通常会将源码包做打包压缩处理，Linux中最常用的打包压缩格式为“tar.gz”，因此源码包又被称为**Tarball**

源码包需要我们自己去软件官方网站进行下载，包中通常包含以下内容：

- 源代码文件。
- 配置和检测程序（如configure或config等）。
- 软件安装说明和软件说明（如INSTALL或README）。



相比源码包，二进制包是在软件发布时已经进行过编译的软件包，所以安装速度比源码包快得多（和Windows下软件安装速度相当）。也正是因为已经进行通译，大家无法看到软件的源代码。



### RPM包的命名规则

RPM 二进制包命名的一般格式如下：

包名-版本号-发布次数-发行商-Linux平台-适合的硬件平台-包扩展名

例如，RPM包的名称是`httpd-2.2.15-15.el6.centos.1.i686.rpm`，其中：

* httped：软件包名。
* 2.2.15：包的版本号，版本号的格式通常为`主版本号.次版本号.修正号`。
* 15：二进制包发布的次数，表示此RPM包是第几次编程生成的。
* el*：软件发行商，el6表示此包是由Red Hat公司发布，适合在RHEL 6.x (Red Hat Enterprise Unux)和CentOS 6.x上使用。
* centos：表示此包适用于CentOS系统。

* i686：表示此包使用的硬件平台，目前的RPM包支持的平台如表所示：

| 平台名称 | 适用平台信息                                                 |
| -------- | ------------------------------------------------------------ |
| i386     | 386 以上的计算机都可以安装                                   |
| i586     | 686 以上的计算机都可以安装                                   |
| i686     | 奔腾 II 以上的计算机都可以安装，目前所有的 CPU 是奔腾 II 以上的，所以这个软件版本居多 |
| x86_64   | 64 位 CPU 可以安装                                           |
| noarch   | 没有硬件限制                                                 |

* rpm：RPM包的扩展名，表明这是编译好的二进制包，可以使用rpm命令直接安装。此外，还有以src.rpm作为扩展名的RPM包，这表明是源代码包，需要安装生成源码，然后对其编译并生成rpm格式的包，最后才能使用rpm命令进行安装。



### RPM包安装卸载（rpm命令）

通常情况下，RPM 包采用系统默认的安装路径，所有安装文件会按照类别分散安装到表 所示的目录中

| 安装路径        | 含 义                      |
| --------------- | -------------------------- |
| /etc/           | 配置文件安装目录           |
| /usr/bin/       | 可执行的命令安装目录       |
| /usr/lib/       | 程序所使用的函数库保存位置 |
| /usr/share/doc/ | 基本的软件使用手册保存位置 |
| /usr/share/man/ | 帮助文件保存位置           |

与RPM包不同，源码包的安装通常采用手动指定安装路径（习惯安装到/usr/local/中）的方式。



**rpm包的安装**

安装 RPM 的命令格式为：

[root@localhost ~]# rpm -ivh 包全名

此命令中各选项参数的含义为：

- -i：安装（install）;
- -v：显示更详细的信息（verbose）;
- -h：打印#，显示安装进度（hash）;

例如，使用此命令安装apache软件包，如下所示：

```
rpm -ivh \
/mnt/cdrom/Packages/httpd-2.2.15-15.el6.centos.1.i686.rpm
```



**RPM包的升级**

[root@localhost ~]# rpm -Uvh包全名

-U（大写）选项的含义是：如果该软件没安装过则直接安装；若已安装则升级至最新版本.



**RPM包卸载**

RPM软件包的卸载要考虑包之间的依赖性。例如，我们先安装的httpd软件包，后安装httpd的功能模块mod_ssl包，那么在卸载时，就必须先卸载mod_ssl，然后卸载httpd，否则会报错。

[root@localhost ~]# rpm -e包名

-e选项表示卸载，也就是erase的首字母



**RPM包查询**

rpm -q：查询软件包是否安装

rpm -qa：查询系统中所有安装的软件包

rpm -qi: 查询软件包详细信息

rpm -ql：命令查询软件包的文件列表

rpm -qf：命令查询系统文件属于哪个RPM包

rpm -qR：查询软件包的依赖关系



### yum详解

yum，全称“Yellow dog Updater, Modified”，是一个专门为了解决包的依赖关系而存在的软件包管理器。就好像Windows系统上可以通过360软件管家实现软件的一键安装、升级和卸载，Linux系统也提供有这样的工具，就是yum。

可以这么说，yum是改进型的RPM软件管理器，它很好的解决了RPM所面临的软件包依赖问题。

yum软件可以用rpm命令安装，安装之前可以通过如下命令查看yum是否已安装

```
rpm -qa | grep yum
```

通过光驱安装yum：

https://jingyan.baidu.com/article/e3c78d6483a02a3c4d85f578.html



**网络 yum 源搭建**

网络yum源配置文件位于/etc/yum.repos.d/

该文件夹下有四个文件：

CentOS-Base.repo

CentOS-Media.repo

CentOS-Debuginfo.repo.bak

CentOS-Vault.repo

一般情况下，

CentOS-Base.repo生效

**本地 yum 源**

在无法联网的情况下，yum可以考虑用本地光盘（或安装映像文件）作为yum源

首先创建挂载点：/mnt/cdrom

将cd挂载到挂载点：mount /dev/cdrom /mnt/cdrom/

修改yum源文件 ： vim CentOS-Media.repo 

baseurl=file:///mnt/cdrom

enabled=1