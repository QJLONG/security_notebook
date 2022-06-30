## Golang_notebook

#### 常量设置(const)

```go
func main() {
	const LENGTH int = 10
	const WIDTH int = 5
	area := LENGTH * WIDTH
	fmt.Println(area)
}
```

#### 特殊常量(iota)

iota 在 const关键字出现时将被重置为 0(const 内部的第一行之前)，const 中每新增一行常量声明将使 iota 计数一次(iota 可理解为 const 语句块中的行索引)。

```go
package main
import "fmt"

func main() {
	const (
		a = iota
		b
		c
		d = 100
		e = iota
	)
	fmt.Println(a, b, c, d, e)
}
```

输出：

```
0 1 2 100 4
```

```go
package main
import "fmt"

const (
	i = 1 << iota
	j = 3 << iota
	k
	l
)

func main() {
	fmt.Println("i=", i)
	fmt.Println("j=", j)
	fmt.Println("k=", k)
	fmt.Println("l=", l)
}
```

输出：

```
i= 1
j= 6
k= 12
l= 24
```

`<<` 是（二进制位）左移的意思

`<<`n == `*`(2^n)



#### 函数

注意：

1. 形参后跟形参类型，否则报错：未定义

2. 函数返回类型，根据真正返回参数的个数而定如：

   ```go
   func swap(x, y string) (string, string) {
   	return y, x
   }
   ```





#### 数组

```go
var balance = [5]float32{1000.0, 2.0, 3.4, 7.0, 50.0}
```

如果数组长度不确定，可以使用 **...** 代替数组的长度，编译器会根据元素个数自行推断数组的长度：

```go
balance := [...]float32{1000.0, 2.0, 3.4, 7.0, 50.0}
```

将索引为 1 和 3 的元素初始化

```
balance := [5]float32{1:2.0,3:7.0}
```





#### 结构体

当结构体类型作为形参时，不管是通过指针引用，还是直接引用，都可以通过类似`book.name`的方访问结构体属性。

```go
package main

import "fmt"

type Books struct {
	name  string
	id    string
	color string
}

func main() {
	var book1 = Books{"HarryPotter", "001", "red"}
	fmt.Println(book1)
	fmt.Printf("Get book name: %s\n", getBookName((&book1)))
	fmt.Printf("Get book id: %s\n", getBookId(book1))
}

// 结构体指针调用
func getBookName(book *Books) string {
	return book.name
}

//结构体直接调用
func getBookId(book Books) string {
	return book.id
}
```





#### 切片

与python中的切片类似，可以截取数组中的一段

除此之外，切片还可以定义容量和长度

```go
package main
import "fmt"

func main() {
	var array1 = [...]int{1, 2, 3, 4, 5}
	var slice1 = array1[0:3]

	//创建容量为5，长度为三的空切片
	var slice2 = make([]int, 3, 5)

	fmt.Println("array1:", array1)
	fmt.Println("slice1:", slice1)
	fmt.Println("slice2:", slice2)

}
```



切片和数组的区别：

数组是值，切片是对数组某一段值的引用

```go
func main() {
	var array = [...]string{"a", "b", "c", "d", "e"}
	var slice1 = array[0:3]
	var slice2 = array[1:4]
	var slice3 = array[2:5]

	fmt.Println(slice1, slice2, slice3)

	slice2[1] = "0"

	fmt.Println(slice1, slice2, slice3)
    //输出silce1的长度和容量
	fmt.Println(len(slice1), cap(slice1))
	
}
```

输出：

```
[a b c] [b c d] [c d e]
[a b 0] [b 0 d] [0 d e]
3 5
```

可以看到，修改slice2中序列号为1的值为0，原数组中的响应位置的值也会发生变化，又因为slice1,slice3也是对原数组的引用，所以也会随之发生变化。



append()的使用

```go
func main() {
	var array []int
	var i int
	for i = 0; i < 10; i++ {
		array = append(array, i)
	}
	fmt.Println(array)
	fmt.Println(len(array), cap(array))
}
```

输出：

```
[0 1 2 3 4 5 6 7 8 9]
10 16
```



#### 利用切片修改字符串中某个字符

Go语言中，字符串无法像C语言中一样直接修改，需要借助切片修改，最后将切片复制给字符串。

```go
func main() {
	s := "hello"
	c := []byte(s)
	c[0] = 'c'
	s = string(c)
	fmt.Println(s)
}
```



#### copy 对切片进行拼接

```go
// 将一个切片插入一个数组的指定index前
func InsertStringSlice(s []int,insertItem []int,index int) []int {
	ns := make([]int,len(s)+len(insertItem))
    //这里at接收copy函数的返回值，用于保存下一次复制的起始位置
    //copy返回复制数组的长度
	at := copy(ns,s[:index])
	at += copy(ns[at:],insertItem)
	copy(ns[at:],s[index:])
	return ns
}

func main() {
	a := []int{1,2,3}
	s := a[:]
	fmt.Println("len:",len(s),"cap:",cap(s),s)
	//s = addLength(s,2)
	s = InsertStringSlice(a,[]int{4,5,6},1)
	fmt.Println("len:",len(s),"cap:",cap(s),s)
}
```

输出：

```
len: 3 cap: 3 [1 2 3]
len: 6 cap: 6 [1 4 5 6 2 3]
```



#### range在循环中的使用

```go
package main
import "fmt"

func main() {
	var array = []int{1, 2, 4, 8, 16, 32, 64, 128}

	//range循环遍历array，其中key为value对应的序号
	for key, value := range array {
		fmt.Print(key, "-", value, " ")
	}
	fmt.Print("\n")
	//如果只想读取key
	for key := range array {
		fmt.Print(key, " ")
	}
	fmt.Print("\n")
	//如果只想读取value，key用"_"代替
	for _, value := range array {
		fmt.Print(value, " ")
	}
	fmt.Print("\n")
}
```

输出：

```
0-1 1-2 2-4 3-8 4-16 5-32 6-64 7-128
0 1 2 3 4 5 6 7
1 2 4 8 16 32 64 128
```





#### map(集合)

```go
package main

import "fmt"

func main() {
	//定义MAP变量
	var countryMap map[string]string
	countryMap = make(map[string]string)
	countryMap["France"] = "巴黎"
	countryMap["China"] = "北京"
	countryMap["Japan"] = "东京"
	countryMap["India"] = "新德里"

	for country := range countryMap {
		fmt.Printf("%s 的首都是：%s\n", country, countryMap[country])
	}
}
```

输出：

```
France 的首都是：巴黎
China 的首都是：北京
Japan 的首都是：东京
India 的首都是：新德里
```



#### 接口

相对于python而言，Golang语言没有类(class)的定义。但是，接口的实现不光能够弥补类的不足，还能够使Golang语言更加灵活。

在结构体上实现了接口后，就可以通过Struct.function()的方式调用接口方法。当一个Struct实现了某个接口上所有的方法时，我们简单地成此结构体实现了该接口。

简单来说，接口是定义在结构体Struct上的，如

```go
package main

import "fmt"

type Phone interface {
	call()
}

type NokiaPhone struct {
}

type IPhone struct {
}

//在结构体NokiaPhone上实现Phone接口
func (nokiaPhone NokiaPhone) call() {
	fmt.Println("I'm nokiaPhone, I can call iphone")
}
//在结构体IPhone上实现Phone接口
func (iphone IPhone) call() {
	fmt.Println("I'm iphone, I can call nokiaPhone")
}

func main() {
	var phone Phone
	phone = new(NokiaPhone)
	phone.call()
	phone = new(IPhone)
	phone.call()
}
```



除此之外，接口还可以用作错误处理：

```go
package main

import "fmt"

type Division struct {
	divisor  int
	dividend int
}

//声明错误接口
type DivisionError interface {
	Error()
}

//实现错误接口
func (de *Division) Error() string {
	var strFormat = `
	Error:
	Can't proceed, the dividend is zero
	divisor:%d
	dividend:0
	`
	return fmt.Sprintf(strFormat, de.divisor)
}

// 实现除法方法
func divide(varDivisor, varDividend int) (int, string) {
	if varDividend == 0 {
		var dData = Division{varDivisor, varDividend}
		var errMsg = dData.Error()
		return 0, errMsg
	} else {
		return varDivisor / varDividend, ""
	}
}

func main() {
	if result, errorMsg := divide(100, 0); errorMsg == "" {
		fmt.Printf("100 / 0 is %d\n", result)
	} else {
		fmt.Println(errorMsg)
	}
}
```

在实现除法的方法时，将错误处理接口的Error()方法实现在了结构体Division上，以实现对Error()方法的直接调用。



#### 并发编程

```GO
package main

import (
	"fmt"
	"time"
)

func say(msg string) {
	var i int
	for i = 0; i < 5; i++ {
		time.Sleep(100 * time.Millisecond)
		fmt.Println(msg)
	}
}

func main() {
	go say("Hello")
	say("World")
}
```

输出:

```
Hello
World
World
Hello
Hello
World
World
Hello
Hello
World
```



#### 通道

通道用于并发线程之间通信：

```go
package main

import "fmt"

func sum(s []int, c chan int) {
	var sum = 0
	for _, value := range s {
		sum += value
	}
	c <- sum
}

func main() {
	var c = make(chan int)
	var s = [...]int{0, 4, 6, 1, 3, 5, 7}
	var slice1 = s[:len(s)/2]
	var slice2 = s[len(s)/2:]
	go sum(slice1, c)
	go sum(slice2, c)
	var x, y = <-c, <-c
	fmt.Println(x, y, x+y)
    close(c)
}
```

输出:

```
16 10 26
```

### 文件读写

#### bufio.NewReader()读取内容

```go
stdinReader := bufio.NewReader(os.Stdin)
msg,err := stdinReader.ReadString('\n')
if err != nil {
    fmt.Println("StdinErr:",err)
}
fmt.Println(msg)
```



#### bufio 按字节读取文件

利用文件对象自带方法实现

读取内容存放在tempByte中

```go
func main() {
	// 打开文件
	file,fileOpenError := os.Open("test.txt")
	if fileOpenError != nil {
		fmt.Println("file open error:",fileOpenError)
	}
	defer file.Close()
	
	//按字节读取文件
	tempByte := make([]byte,4)
	for {
		_,readerr := file.Read(tempByte)
		if readerr != nil {
			if readerr == io.EOF {
				break
			} else {
				fmt.Println("read error:",readerr)
			}
		}
		fmt.Println((tempByte))
	}
}
```



#### bufio按行读取文件

```go
func main() {
	// 打开文件
	file,fileOpenError := os.Open("test.txt")
	if fileOpenError != nil {
		fmt.Println("file open error:",fileOpenError)
	}
	defer file.Close()

	readreader := bufio.NewReader(file)

	for {
		line,_,readerr := readreader.ReadLine()
		if readerr != nil {
			if readerr == io.EOF {
				break
			} else {
				fmt.Println("read error:",readerr)
			}
		}
		fmt.Println(string(line))
	}
}
```



#### os.open()打开文件

```go
file,fileOpenErr := os.Open("test.txt")
if fileOpenErr != nil {
    fmt.Println("File open error:",fileOpenErr)
}
defer file.Close()
```



#### ioutil读取文件内容

1. 需要先打开文件

```go
func main() {
	file,fileOpenError := os.Open("test.txt")
	if fileOpenError != nil {
		fmt.Println("file open error:",fileOpenError)
	}
	// 读取文件内容
	content,readErr := ioutil.ReadAll(file)
	if readErr != nil {
		fmt.Println("read error:",readErr)

	}
	fmt.Println(string(content))
}
```

2. 不需要先打开文件

```go
func main() {
	content,readerr := ioutil.ReadFile("test.txt")
	if readerr != nil {
		fmt.Println("Read error:",readerr)
	}
	fmt.Println(string(content))
}
```

