### Docker 安装

这里使用的是Ubuntu系统

* 查看是否已经安装docker

  ```shell
  dpkg -s docker
  ```

  ![](https://hummer-vin.oss-cn-beijing.aliyuncs.com/images/20220514095159.png)

  这里的ubuntu并没有安装docker

  如果安装了docker，要先卸载旧版本的docker

  ```shell
  sudo apt-get remove docker docker-engine docker.io containerd runc
  ```

* 使用国内daocloud一键安装命令

  ```shell
  curl -sSL https://get.daocloud.io/docker | sh
  ```

* 手动安装方法：

  参考：[Docker实践(一):Ubuntu16.04安装Docker - 云+社区 - 腾讯云 (tencent.com)](https://cloud.tencent.com/developer/article/1501447)
  
  * **允许apt命令可以使用HTTPS访问Docker repository**
  
    ```shell
    apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
    ```
  
  * **添加Docker官方的GPG key**
  
    ```shell
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    ```
  
    验证key
  
    ```shell
    apt-key fingerprint 0EBFCD88
    ```
  
  * **设置repository版本为stable并更新软件列表**
  
    ```shell
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    
    apt-get update
    ```
  
  * **安装Docker CE和containerd**
  
    ```shell
    apt-get install docker-ce docker-ce-cli containerd.io
    ```
  
  * 查看docker版本
  
    ```shell
    docker --version
    ```
  
    

