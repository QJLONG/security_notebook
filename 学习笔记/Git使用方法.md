## Git使用方法

#### 一、Git是什么？

Git是目前世界上最先进的分布式版本控制系统。
工作原理 / 流程：

![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/v2-3bc9d5f2c49a713c776e69676d7d56c5_r.jpg)

​	Workspace：工作区	

​	Index / Stage：暂存区
​	Repository：仓库区（或本地仓库）
​	Remote：远程仓库

#### 二、SVN与Git的区别

SVN是**集中式**版本控制系统，版本库是**集中放在中央服务器**的，而干活的时候，用的都是自己的电脑，所以首先要从中央服务器哪里得到最新的版本，然后干活，干完后，需要把自己做完的活推送到中央服务器。集中式版本控制系统是必须联网才能工作，如果在局域网还可以，带宽够大，速度够快，如果在互联网下，如果网速慢的话，就纳闷了。

Git是**分布式**版本控制系统，那么它就**没有中央服务器**的，每个人的电脑就是一个完整的版本库，这样，工作的时候就不需要联网了，因为版本都是在自己的电脑上。既然每个人的电脑都有一个完整的版本库，那多个人如何协作呢？比如说自己在电脑上改了文件A，其他人也在电脑上改了文件A，这时，你们两之间只需把各自的修改推送给对方，就可以互相看到对方的修改了。

#### 三、WIndows版本下载地址：

https://github.com/git-for-windows/git/releases/download/v2.36.0.windows.1/Git-2.36.0-64-bit.exe

安装完成后需要首先配置用户名和邮箱作为自己的标识

配置命令如下：

```
git config --global user.name=""
git config --global user.email=""
```

git config --global 参数，有了这个参数，表示你这台机器上所有的Git仓库都会使用这个配置，当然你也可以对某个仓库指定的不同的用户名和邮箱。

#### 四、具体操作

1. 创建版本库

   什么是版本库？版本库又名仓库，英文名repository,你可以简单的理解一个目录，这个目录里面的所有文件都可以被Git管理起来。

   ```shell
   mkdir testgit
   ```

   对版本库进行初始化

   ```shell
   git init
   ```

   这时候你当前testgit目录下会多了一个.git的目录，这个目录是Git来跟踪管理版本的，没事千万不要手动乱改这个目录里面的文件，否则，会把git仓库给破坏了。

2. 将文件添加到版本库中

   首先要明确下，所有的版本控制系统，只能跟踪文本文件的改动，比如txt文件，网页，所有程序的代码等，Git也不列外，版本控制系统可以告诉你每次的改动，但是图片，视频这些二进制文件，虽能也能由版本控制系统管理，但没法跟踪文件的变化，只能把二进制文件每次改动串起来，也就是知道图片从1kb变成2kb，但是到底改了啥，版本控制也不知道。

   例如：

   在testgit目录下新建一个txt文件，内容为“hummer”

   ```
   echo hummer > test.txt
   ```

   

   * 使用命令 git add readme.txt添加到暂存区里面去

     ```
     git add test.txt
     ```

     

   * 用命令 git commit告诉Git，把文件提交到仓库。

     ```
     git commit -m "test.txt已经提交"
     ```

     

   * 查看文件提交情况

     ```
     git status
     ```

   * 修改以下test.txt文件再次查看提交情况

     ![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220507091016.png)

     查看修改了哪些内容

     ```shell
     git diff test.txt
     ```

     

   * 再次add，commit

3. 版本回退

   再修改以下test.txt文件

   ![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220507091559.png)

   用git log命令查看以下历史记录

   ![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220507091757.png)

   如果嫌上面显示的信息太多的话，我们可以使用命令 git log --pretty=oneline 演示如下：

   ![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220507091942.png)

   现在我想使用版本回退操作，我想把当前的版本回退到上一个版本，要使用什么命令呢？可以使用如下2种命令，第一种是：**git reset --hard HEAD^** 那么如果要回退到上上个版本只需把HEAD^ 改成 HEAD^^ 以此类推。那如果要回退到前100个版本的话，使用上面的方法肯定不方便，我们可以使用下面的简便命令操作：**git reset --hard HEAD~100** 即可。

   ```
   git reset --hard HEAD^		回退到上一个版本
   git reset --hard HEAD~100	回退到前100个版本
   ```

   除此之外也可以用版本后退

   版本号可以通过 git log 获取

   ```
   git reset --hard  版本号
   ```

   ![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220507093055.png)

   如果我们想回到最新的版本

   

   可以通过 git reflog 获取回退前的版本号，然后通过版本号回退

   ```
   git reflog
   ```

4. 如果文件没有提交到暂存区（git add），可以通过 git checkout -- filename来撤销对工作区中文件的修改，当然，也可以用来回复已经删除的文件，前提是还没有commit

   注意：文件名前也有一个空格

   ```git
   git checkout -- filename
   ```

   

 5. 远程仓库

    * 在了解之前，先注册github账号，由于你的本地Git仓库和github仓库之间的传输是通过SSH加密的，所以需要一点设置：
      第一步：创建SSH Key。在用户主目录下，看看有没有.ssh目录，如果有，再看看这个目录下有没有id_rsa和id_rsa.pub这两个文件，如果有的话，直接跳过此如下命令，如果没有的话，打开命令行，输入如下命令：

    * ```git
      ssh-keygen -t rsa –C "youremail@example.com"
      ```

      

      ![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220507095941.png)

      创建密钥完成后如上图，其中id_rsa是私钥,id_rsa.pub是公钥

      将公钥粘贴到github中完成绑定

    

    * 在github创建远程仓库后，将本地仓库与github远程仓库关联

      然后将本地仓库的内容推送到GitHub中 

      ```
      git remote add origin https://github.com/QJLONG/python_notebook.git
      ```

      

      如果出现如下错误信息

      ![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220507105431.png)

      那是因为本地没有update到最新版本的项目（git上有README.md文件没下载下来）

      解决方法：

      ```
      git pull --rebase origin master
      ```

      

    

    