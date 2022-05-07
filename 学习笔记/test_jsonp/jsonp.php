<!-- /*
 * @Description: 
 * @Autor: hummer
 * @Date: 2022-04-28 19:25:54
 * @LastEditors: hummer
 * @LastEditTime: 2022-04-28 20:05:06
 */ -->
<?php
//获取回调函数名
$jsoncallback = htmlspecialchars($_REQUEST['jsoncallback']);

//json数据
$json_data = '["customername1","customername2"]';

//输出jsonp格式的数据
echo $jsoncallback . "(" . $json_data . ")";
?>
