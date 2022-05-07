---
title: BugkuCTF web18_秋名山车神
date: 2022-1-5 18:03:50
updated: 2022-1-5 18:03:50
categories: 渗透练习
tags: ctf
urlname:
keywords: ctf,BugkuCTF,秋名山车神
---

### BugkuCTF web18_秋名山车神 writeup



![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220105175453.png)

<br>

表达式的值需要在两秒钟计算出来，我们可以利用session来保持会话

```python3
import requests  # 引入request库
import re  # 引入re库

url = 'http://114.67.175.224:17452'
s = requests.session()  # 用session会话保持表达式
return_html = s.get(url)

equation = re.search(r'(\d+[+\-*])+(\d+)', return_html.text).group()
result = eval(equation)  # eval()函数用来执行一个字符串表达式,并返回表达式的值。

key = {'value': result}  # 创建一个字典类型用于传参
flag = s.post(url, data=key)  # 用post方法传上去

print(flag.text)
```

此段代码中重要部分在第六行的正则表达式：

```\d+```表示匹配一个或者多个数字。```[+\-*]```匹配一个加号或者减号或者乘号，其中减号为转义字符，其前面需要加上反斜杠。

post传输的参数名称（value）在多次刷新后会给出提示。

由于python计算的结果和php计算的结果可能会有偏差，所以有一定概率能够的到正确的结果，获得flag，多次尝试即可。

<br>

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220105175536.png)

<br>

![](https://cdn.jsdelivr.net/gh/QJLONG/HUMMER-PIC@master/img/20220105180043.png)