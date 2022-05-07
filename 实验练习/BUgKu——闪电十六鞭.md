---
title: BUgKu——闪电十六鞭
date: 2022-1-13 10:07:50
updated: 2022-1-13 10:07:50
categories: 渗透练习
tags: ctf
urlname:
keywords: ctf,BugkuCTF,闪电十六鞭
---

### BUgKu——闪电十六鞭

题目给出的php代码如下：

```php
<?php
    error_reporting(0);
    require __DIR__.'/flag.php';

    $exam = 'return\''.sha1(time()).'\';';

    if (!isset($_GET['flag'])) {
        echo '<a href="./?flag='.$exam.'">Click here</a>';
    }
    else if (strlen($_GET['flag']) != strlen($exam)) {
        echo '长度不允许';
    }
    else if (preg_match('/`|"|\.|\\\\|\(|\)|\[|\]|_|flag|echo|print|require|include|die|exit/is', $_GET['flag'])) {
        echo '关键字不允许';
    }
    else if (eval($_GET['flag']) === sha1($flag)) {
        echo $flag;
    }
    else {
        echo '马老师发生甚么事了';
    }

    echo '<hr>';

    highlight_file(__FILE__);
```

这里解释一下：

题目要求给出get请求参数flag并满足一下条件：
①长度与$exam的长度相等，这里我们可以通过输出\$exam的长度来确定

```php
<?php
    $exam = 'return\''.sha1(time()).'\';';
    echo strlen($exam);
?>
```

输出结果是49，也就意味着给出参数flag的长度也应为49。

②给出的参数的值中不能含有关键字：‘，“，.,\\,(,),[,],_,flag,echo,print,require,include,die,exit,is

③在第三处if语句中我们看到的eval函数，我们可以通过这个函数来进行短标签绕过，具体绕过方法如下：

```php
?flag=$a='blag';$a{0}='f';?>11111111111111111;<?=$$a;?>
```

其中：

{}代替了[]

<?=$$a;?>与<?php echo $$a;?>具有相同的效果

中间的1是为了填充长度



