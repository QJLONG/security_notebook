## XMLHttpRequest对象

**创建对象**

```javascritp
var xmlhttp;
if (window.XMLHttpRequest){
	//  IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
	var xmlhttp = new XMLHttpRequest();
}
else{
    // IE6, IE5 浏览器执行代码
    xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
}
```



**建立连接**

```js
xmlhttp.open(method,url,async,username,password);
```

* async:是否开启异步方式，默认为True,如果为 false，当状态改变时会立即调用 onreadystatechange 属性指定的回调函数。
* username:可选参数，如果服务器需要验证，该参数指定用户名，如果未指定，当服务器需要验证时，会弹出验证窗口。
* password：可选参数，验证信息中的密码部分，如果用户名为空，则该值将被忽略。

**设置请求头**

```js
xmlhttp.setRequestHeader('Content-type':'application/x-www-form-urlencoded');
```



**发送请求**

```js
xmlhttp.send(body);
```

body:发送请求时的数据部分(data)，如果不传递信息，可以设置为null或省略

发送请求后，可以使用 XMLHttpRequest 对象的 responseBody、responseStream、responseText 或 responseXML 属等待接收响应数据。

例如：

```js
var xhr = creatXHR();  //实例化XMLHttpRequest 对象
xhr.open ("GET", "server.txt", false");  //建立连接
xhr.send(null);  //发送请求
console.log(xhr.responseText);  //接收数据
```



**异步响应状态**

在 JavaScript 中，使用 readyState 属性可以实时跟踪异步响应状态。当该属性值发生变化时，会触发 readystatechange 事件，调用绑定的回调函数。readyState 属性值说明如表所示。

| 返回值 | 说明                                                         |
| ------ | ------------------------------------------------------------ |
| 0      | 未初始化。表示对象已经建立，但是尚未初始化，尚未调用open()方法 |
| 1      | 初始化。表示对象已经建立，尚未调用 send() 方法               |
| 2      | 发送数据。表示 send() 方法已经调用，但是当前的状态及 HTTP 头未知 |
| 3      | 数据传送中。已经接收部分数据，因为响应及 HTTP 头不安全，这时通过 responseBody 和 responseText 获取部分数据会出现错误 |
| 4      | 完成。数据接收完毕，此时可以通过 responseBody 和 responseText 获取完整的响应数据 |

如果 readyState 属性值为 4，则说明响应完毕，那么就可以安全的读取响应的数据。

考虑到各种特殊情况，更安全的方法是同时监测 HTTP 状态码，只有当 HTTP 状态码为 200 时，才说明 HTTP 响应顺利完成。

例如：

```js
<!--
 * @Description: 
 * @Autor: hummer
 * @Date: 2022-04-29 19:53:09
 * @LastEditors: hummer
 * @LastEditTime: 2022-04-29 20:13:21
-->
<!DOCTYPE>
<html>
<head>
<meta charset="utf-8">
<script>

window.onload = function(){
    var b = document.getElementById("input");
    b.onclick=function(){

        var url = "server.php";
        var xhr = new XMLHttpRequest();
        // xhr.setRequestHeader('Content-type','application/x-www-form-urlencoded');
        xhr.open('POST',url,true);
        xhr.onreadystatechange = function(){
            if(xhr.readyState==4 && xhr.status==200){
                console.log(xhr.responseText);
                document.getElementById("myDiv").innerHTML=xhr.responseText;
            }
        }
        xhr.send();
    }
    
}

</script>
</head>
<body>
    <button id="input">发起请求
    </button>
    <div id="myDiv"></div>
</body>
</html>
```

该页面通过点击按钮发送请求获取server.php中的内容



**获取XML数据**

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220429201924.png)

示例：

```js
<input name="submit" type="button" id="submit" value="向服务器发出请求" />
<script>
    window.onload = function () {  //页面初始化
        var b = document.getElementsByTagName("input")[0];
        b.onclick = function () {
            var xhr = createXHR();  //实例化XMLHttpRequest对象
            xhr.open("GET", "server.xml", true);  //建立连接，要求异步响应
            xhr.onreadystatechange = function () {  //绑定响应状态事件监听函数
                if (xhr.readyState == 4) {  //监听readyState状态
                    if (xhr.state == 200 || xhr.status == 0) {  //监听HTTP状态码
                        var info = xhr.responseXML;
                        console.log(info.getElementsByTagName("the")[0].firstChild.data);  //返回元信息字符串“XML 数据”
                    }
                }
            }
            xhr.send();  //发送请求
        }
    }
</script>
```

使用服务器端脚本生成 XML 结构数据。

server.php

```php
<?php
    header('Content-Type: text/html;');
    echo '<?xml version="1.0" encoding="utf-8"?><the>XML 数据</the>';  //输出XML
?>
```



**获取和设置头部字段**

```js
console.log(xhr.getAllResponseHeaders());
console.log(xhr.getResponseHeader("Content-Type"));

xhr.setResponseHeader("Header-name", "value");
xhr.setResponseHeader("Content-Type", "application/x-www-form-urlencoded");
```

