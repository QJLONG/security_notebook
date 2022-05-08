## Shell编程



linux 其他命令

进入 Linux 终端，编写一个 Shell 脚本 hello.sh 

```shell
#!/bin/bash
echo "hello world!"
```

运行：

```shell
# 方法1
sh shell.sh
# 方法2
chmod +x shell.sh
./shell.sh
```

- `#!` 告诉系统这个脚本需要什么解释器来执行。
- 文件扩展名 `.sh` 不是强制要求的。
- 方法1 直接运行解释器，`hello.sh` 作为 Shell 解释器的参数。此时 Shell 脚本就不需要指定解释器信息，第一行可以去掉。
- 方法2 hello.sh 作为可执行程序运行，Shell 脚本第一行一定要指定解释器。



#### **Shell变量**

* **定义**：变量名=变量值，等号两侧不能有空格，变量名一般习惯用大写
* **删除变量：**unset 变量名
* **声明静态变量：**readonly 变量名，静态变量不能unset
* **使用变量：**$变量名
* **将命令返回值赋给变量（重点）**
  - A=\`ls\` 反引号,执行里面的命令
  - A=$(ls) 等价于反引号



#### **Shell 环境变量**
**定义**

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/v2-42d4bc4444463d62135b3508aa4ad7f3_720w.jpg)

**基本语法**

1. export 变量名=变量值，将 Shell 变量输出为环境变量。

2. source 配置文件路径，让修改后的配置信息立即生效。

3. echo $变量名，检查环境变量是否生效

   

#### **参数位置变量**
**基本语法**

- $n ：$0 代表命令本身、$1-$9 代表第1到9个参数，10以上参数用花括号，如 ${10}。
- $* ：命令行中所有参数，且把所有参数看成一个整体。
- $@ ：命令行中所有参数，且把每个参数区分对待。
- $# ：所有参数个数。
- $\*与$@的区别：$\*与$@不被引号包围时没有任何区别，但被引号包围时，`"$*"`会将所有的参数从整体上看做一份数据，而不是把每个参数都看做一份数据。`"$@"`仍然将每个参数都看作一份数据，彼此之间是独立的。两者的区别只凭打印输出是看不出区别的，但通过for 循环就能很清晰的看出来（具体实例见后面for循环）

**实例：**
编写 Shell 脚本 positionPara.sh ，输出命令行输入的各个参数信息。

```bash
#!/bin/bash     
# 输出各个参数 
echo $0 $1 $2 
echo $* 
echo $@ 
echo 参数个数=$#
```


运行：

```bash
chmod +x positionPara.sh 
./positionPara.sh 10 20
```


运行结果：

```bash
./positionPara.sh 10 20 
10 20 
10 20 
参数个数=2
```



#### 预定义变量

**定义**
在赋值定义之前，事先在 Shell 脚本中直接引用的变量。
**基本语法**

- $$ ：当前进程的 PID 进程号。
- $! ：后台运行的最后一个进程的 PID 进程号。
- $? ：最后一次执行的命令的返回状态，0为执行正确，非0执行失败。



#### **运算符**
**基本语法**

- $((运算式)) 或 $[运算式]
- expr m + n 注意 expr 运算符间要有空格
- expr m - n
- expr \*，/，% 分别代表乘，除，取余

**实例**

```bash
# 第1种方式 $(()) 
echo $(((2+3)*4))   

# 第2种方式 $[]，推荐 
echo $[(2+3)*4]  

# 使用 expr 
TEMP=`expr 2 + 3` 
echo `expr $TEMP \* 4`
```



#### **条件判断**

**基本语法**
[ condition ] 注意condition前后要有空格。非空返回0，0为 true，否则为 false 。

**实例**

```bash
#!/bin/bash 
if [ 'test01' = 'test' ] 
then
     echo '等于' 
fi  

# 20是否大于10 
if [ 20 -gt 10] 
then
     echo '大于' 
fi  

# 是否存在文件/root/shell/a.txt 
if [ -e /root/shell/a.txt ] 
then
     echo '存在' 
fi  

if [ 'test02' = 'test02' ] && echo 'hello' || echo 'world' 
then
     echo '条件满足，执行后面的语句' 
fi
```


运行结果：

```bash
大于 
hello 
条件满足，执行后面的语句
```

####  case 分支

**基本语法**

```bash
case $变量名 in
"值1")
如果变量值等于值1，则执行此处程序1
;;
"值2")
如果变量值等于值2，则执行此处程序2
;;
...省略其它分支...
*)
如果变量值不等于以上列出的值，则执行此处程序
;;
esac
```

**实例**

当命令行参数为1时输出“周一”，2时输出“周二”，其他情况输出“其它”。

```bash
case $1 in
"1")
echo 周一
;;
"2")
echo 周二
;;
*)
echo 其它
;;
esac
```



#### **for 循环**

**基本语法**

```bash
# 语法1
for 变量名 in 值1 值2 值3...
do
    程序
done

# 语法2
for ((初始值;循环控制条件;变量变化))
do
    程序
done
```

**实例**

打印\$\*与\$@的区别

```shell
#!/bin/bash
# print all parameters at the terminal

# method 1
for i in "$@"
do
        echo "the arg by \$@ is $i"
done
echo "====================="


# method 2
for j in "$*"
do
        echo "the arg by \$* is $j"
done
```

运行结果

```
hummer@hummer-virtual-machine:~/shell$ ./for.sh 1 2 3
the arg by $@ is 1
the arg by $@ is 2
the arg by $@ is 3
=====================
the arg by $* is 1 2 3
hummer@hummer-virtual-machine:~/shell$ 
```

运用迭代器表达式实现for循环：

```shell
#!/bin/bash
# add from 1 to 100
SUM=0
for ((i=1;i<=100;i++))
do
        SUM=$[$SUM+$i]
done
echo $SUM
```



#### while 循环

```shell
#!/bin/bash
# add from 1 to 100
SUM=0
i=0
while [ $i -le 100 ]
do
        SUM=$[$SUM+$i]
        i=$[$i+1]
done
echo $SUM
```

-eq      //等于

-ne      //不等于

-gt      //大于

-lt      //小于

ge      //大于等于

le      //小于等于



#### **读取控制台输入**

**基本语法**

read(选项)(参数)
**选项**

- -p：指定读取值时的提示符
- -t：指定读取值时等待的时间（秒），如果没有在指定时间内输入，就不再等待了。

**参数**

- 变量名：读取值的变量名

**实例**

```shell
#!/bin/bash
# read a parameter from terminal
read -p "please input a parameter here: num1=" NUM1
echo "your parameter is num1=$NUM1"

read -t 10 -p "please input a parameter in 10 seconds: num2=" NUM2
echo "your parameter is num2=$NUM2"
```

#### 函数

**系统函数**

- basename，删掉路径最后一个 / 前的所有部分（包括/），常用于获取文件名。
  **基本语法**

- - basename [pathname] [suffix]
  - basename [string] [suffix]
  - 如果指定 suffix，也会删掉pathname或string的后缀部分。

- **实例**

- ```shell
  hummer@hummer-virtual-machine:~/shell$ basename /usr/bin/sort
  sort
  hummer@hummer-virtual-machine:~/shell$ basename /usr/bin/sort.sh
  sort.sh
  hummer@hummer-virtual-machine:~/shell$ basename /usr/bin/sort.sh .sh
  sort
  hummer@hummer-virtual-machine:~/shell$
  ```

- 

- dirname，删掉路径最后一个 / 后的所有部分（包括/），常用于获取文件路径。
  **基本语法**

- - dirname pathname

  - 如果路径中不含 / ，则返回 '.' （当前路径）。

  - **实例**

    ```bash
    # dirname /usr/bin/  
    /usr  
    
    # dirname dir1/str dir2/str 
    dir1 
    dir2  
    
    # dirname stdio.h 
    .
    ```

**自定义函数**

**基本语法**

```bash
[ function ] funname[()]
{
    Action;
    [return int;]
}

# 调用
funname 参数1 参数2...
```

**实例**

```shell
#!/bin/bash
# create a function to calculate the sum of two numbers
function getSum(){
        SUM=$[$NUM1+$NUM2]
        echo "sum=$SUM"
}

read -p "please input n1=" NUM1
read -p "please input n2=" NUM2

# 调用函数
getSum $NUM1 $NUM2
```

运行结果

```
hummer@hummer-virtual-machine:~/shell$ ./function.sh 
please input n1=20
please input n2=40
sum=60
```



#### 其他

1. 字符串拼接问题

   ```shell
   #!/bin/bash
   name="Shell"
   url="http://c.biancheng.net/shell/"
   str1=$name$url  #中间不能有空格
   str2="$name $url"  #如果被双引号包围，那么中间可以有空格
   str3=$name": "$url  #中间可以出现别的字符串
   str4="$name: $url"  #这样写也可以
   str5="${name}Script: ${url}index.html"  #这个时候需要给变量名加上大括号
   echo $str1
   echo $str2
   echo $str3
   echo $str4
   echo $str5
   ```

   运行结果

   ```
   运行结果：
   Shellhttp://c.biancheng.net/shell/
   Shell http://c.biancheng.net/shell/
   Shell: http://c.biancheng.net/shell/
   Shell: http://c.biancheng.net/shell/
   ShellScript: http://c.biancheng.net/shell/index.html
   ```

   