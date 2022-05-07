## Cross Site Scripting

一句话，XSS就是在用户的浏览器中执行攻击者自己定制的脚本。

### 反射型（不持久型）(中危)

反射性XSS，也就是非持久性XSS。用户点击攻击链接，服务器解析后响应，在返回的响应内容中出现攻击者的XSS代码，被浏览器执行。一来一去，**XSS攻击脚本被web server反射回来给浏览器执行**，所以称为反射型XSS。

特点：

1> XSS攻击代码非持久性，也就是没有保存在web server中，而是出现在URL地址中；

2> 非持久性，那么攻击方式就不同了。一般是攻击者通过邮件，聊天软件等等方式发送攻击URL，然后用户点击来达到攻击的；

```php
<?php
    $name = $_GET['name'];
    echo "Welcome $name<br>";
?>
```



### 存储型（高危）

区别就是XSS恶意代码**存储在web server中**，这样，每一个访问特定网页的用户，都会被攻击。

特点：

1> XSS攻击代码存储于web server上；

2> 攻击者，一般是通过网站的留言、评论、博客、日志等等功能(所有能够向web server输入内容的地方)，将攻击代码存储到web server上的；

有时持久性XSS和反射型XSS是同时使用的，比如先通过对一个攻击url进行编码(来绕过xss filter)，然后提交该web server(存储在web server中), 然后用户在浏览页面时，如果点击该url，就会触发一个XSS攻击。当然用户点击该url时，也可能会触发一个CSRF(Cross site request forgery)攻击。



### DOM XSS

基于DOM的XSS，**也就是web server不参与，仅仅涉及到浏览器的XSS**。比如根据用户的输入来动态构造一个DOM节点，如果没有对用户的输入进行过滤，那么也就导致XSS攻击的产生。过滤可以考虑采用**esap**

```php
' onclick="alert(123)">
```



###  XSS 存在的原因

XSS 存在的根本原因是，对URL中的参数，对用户输入提交给web server的内容，没有进行充分的过滤。如果我们能够在web程序中，对用户提交的URL中的参数，和提交的所有内容，进行充分的过滤，将所有的不合法的参数和输入内容过滤掉，那么就不会导致“在用户的浏览器中执行攻击者自己定制的脚本”。



### 常用测试语句

```html
<script>alert(1)</script>
<img src=x onerror=alert(1) />
<svg onload=alert(1) />
<a href=javascript:alert(1) />
```



### xss测试工具：XSSER

```shell
sudo atp-get install xsser
xsser -u "http://10.10.10.137/dvwa/vulnerabilities/xss_r/?name=XSS" --cookie "security=low; security=low; PHPSESSID=8f91af9ebda06bd2af89558a7758e9a2"
```

```
[+] Target: http://10.10.10.137/dvwa/vulnerabilities/xss_r/?name=XSS
[+] Vector: [ name ]
[!] Method: URL
[*] Hash: 771d45d2a33569793b37527f3552a58f
[*] Payload: http://10.10.10.137/dvwa/vulnerabilities/xss_r/?name=%22%3E771d45d2a33569793b37527f3552a58f
[!] Vulnerable: [IE7.0|IE6.0|NS8.1-IE] [NS8.1-G|FF2.0] [O9.02]
[!] Status: XSS FOUND! [WITHOUT --reverse-check VALIDATION!] 
```



### XSS防御

参考：[XSS 防御方法总结 - digdeep - 博客园 (cnblogs.com)](https://www.cnblogs.com/digdeep/p/4695348.html#:~:text=XSS 攻击的防御 XSS防御的总体思路是： 对输入,(和URL参数)进行过滤，对输出进行编码 。 也就是对提交的所有内容进行过滤，对url中的参数进行过滤，过滤掉会导致脚本执行的相关内容；然后对动态输出到页面的内容进行html编码，使脚本无法在浏览器中执行。 虽然对输入过滤可以被绕过，但是也还是会拦截很大一部分的XSS攻击 。)

XSS防御的总体思路是：**对输入(和URL参数)进行过滤，对输出进行编码**。

1. 对输入和URL参数进行过滤(白名单和黑名单)

   

   Java语言中提供了 OWASP ESAPI专门用来防御安全漏洞，其中包括XSS的防御：

   * HTML编码：

     ```java
     String str = ESAPI.encoder().encodeFOrHTML(String input);
     ```

     这个接口采用的编码器是HTMLEntityCodec。如果是空格，字母或者是数字，就不编码，如果有特殊字符就替换为HTML实体（规则与PHP相同）

     OWASP还有专门应对HTML属性的编码操作，其接口如下：

     ```java
     String str = ESAPI.encoder().encodeFORHTMLAttribute(Sting input);
     ```

     

   * CSS编码

     接口如下：

     ```java
     String str = ESAPI.encoder().encodeForCSS(String input);
     ```

     CSS编码器是CSSCocec，编码原理是通过反斜杠(\\)加上十六进制进行编码

   * JavaScript编码

     接口如下：

     ```java
     String str = ESAPI.encoder().encodeForJavaScript(Sting input);
     ```


2. 对输出进行过滤

   在输出数据之前对潜在的威胁的字符进行编码、转义是防御XSS攻击十分有效的措施。如果使用好的话，理论上是可以防御住所有的XSS攻击的。

   对所有要动态输出到页面的内容，通通进行相关的编码和转义。当然转义是按照其输出的上下文环境来决定如何转义的。

   **1>** 作为body文本输出，作为html标签的属性输出：

   比如：<span>${username}</span>, <p><c:out value="${username}"></c:out></p>

   <input type="text" value="${username}" />

   此时的转义规则如下：

   < 转成 `&lt`;

   \> 转成 `&gt`;

   & 转成 `&amp`;

   " 转成 `&quot`;

   ' 转成 `&#39`

   **2>** javascript事件

   <input type="button" onclick='go_to_url("${myUrl}");' />

   除了上面的那些转义之外，还要附加上下面的转义：

   \ 转成`` \\``

   / 转成`` \/``

   ; 转成 ；(全角;)

   **3>** URL属性

   如果 `<script>`, `<style>`, `<imt> `等标签的 src 和 href 属性值为动态内容，那么要确保这些url没有执行恶意连接。

   确保：href 和 src 的值必须以 http://开头，白名单方式；不能有10进制和16进制编码字符。

3. HttpOnly

   HttpOnly对XSS漏洞不起作用，主要目的是解决Cookie劫持问题

   JavaScript将不能获取带有HttpOnly属性的Cookie。

   一般的Cookie都是从document对象中获得的，现在浏览器在设置 Cookie的时候一般都接受一个叫做HttpOnly的参数，跟domain等其他参数一样，一旦这个HttpOnly被设置，**你在浏览器的 document对象中就看不到Cookie了，而浏览器在浏览的时候不受任何影响**，因为Cookie会被放在浏览器头中发送出去(包括ajax的时 候)，应用程序也一般不会在js里操作这些敏感Cookie的，对于一些敏感的Cookie我们采用HttpOnly，对于一些需要在应用程序中用js操作的cookie我们就不予设置，这样就保障了Cookie信息的安全也保证了应用。

   ![](https://s2.loli.net/2022/03/21/sHtLW7v3peEkCRD.png)

4. CSP 来防御 XSS

   相关介绍：

   https://content-security-policy.com/
   https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Headers/Content-Security-Policy

   

   CSP基本原理是限制浏览器只加载我们配置指定来源的资源，比如只加载我们自己网站的js和CDN中的js，避免加载XSS攻击时攻击者指定的攻击来源的资源，从而减轻XSS的攻击风险

   

    在nginx的server{}段加入下面的配置：

   add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval';font-src 'self' data:; img-src 'self' data: 'unsafe-inline' https:; style-src 'self' 'unsafe-inline';frame-ancestors 'self'; frame-src 'self';connect-src https:";

   上面的配置，使用CSP的指令来指定浏览器可以加载哪些来源的资源（js、css、img等等），其他来源资源都会被浏览器拒绝。具体CSP指令的含义参考上面的URL连接。

   

5. **X-Frame-Options 响应头** 
   X-Frame-Options HTTP 响应头是用来给浏览器指示允许一个页面可否在 <frame>, </iframe> 或者 <object> 中展现的标记。网站可以使用此功能，来确保自己网站的内容没有被嵌到别人的网站中去，也从而避免了点击劫持 (clickjacking) 的攻击。

   **使用 X-Frame-Options** 
   X-Frame-Options 有三个值:

   **DENY** 
   表示该页面不允许在 frame 中展示，即便是在相同域名的页面中嵌套也不允许。 
   **SAMEORIGIN** 
   表示该页面可以在相同域名页面的 frame 中展示。 
   **ALLOW-FROM uri** 
   表示该页面可以在指定来源的 frame 中展示。 
   换一句话说，如果设置为 DENY，不光在别人的网站 frame 嵌入时会无法加载，在同域名页面中同样会无法加载。另一方面，如果设置为 SAMEORIGIN，那么页面就可以在同域名页面的 frame 中嵌套。