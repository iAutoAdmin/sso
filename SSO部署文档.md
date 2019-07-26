# autoadmin项目SSO部署文档

## 作者信息
```
cheng.qi
782118373@qq.com
```
## 服务器部署配置说明

```
##CPU： 2核
##内存： 4 GiB
##实例类型： I/O优化
##操作系统： CentOS 7.6 64位
##硬盘    40GB
##带宽    1Mbps
##阿里云IP     172.17.119.254
```
注：如部署iAutoAdmin其余项目已配置过基础环境，可直接从第（4）步开始操作


1)安装docker-ce与mysql数据库

```
yum-config-manager --add-repo \https://download.docker.com/linux/centos/docker-ce.repo
yum install wget lrzsz docker-ce -y
systemctl start docker && systemctl enable docker
cd /tmp/ && wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm
rpm -ivh mysql-community-release-el7-5.noarch.rpm
yum install mysql-server -y
systemctl start mysqld
mysqladmin -u root password 123456

```

2)# 安装编译依赖

```
yum install   sqlite-devel bzip2-devel bzip2-libs  readline readline-devel readline-static   openssl openssl-devel openssl-static gdbm-devel  gcc make patch  openssl-devel sqlite-devel readline-devel zlib-devel bzip2-devel libffi-devel  -y 
curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
cat << EOF >> ~/.bash_profile 
export PATH="~/.pyenv/bin:\$PATH"
eval "\$(pyenv init -)"
eval "\$(pyenv virtualenv-init -)"
EOF

source ~/.bash_profile 
```

3)# 编译安装Python 3.7.2 for centos 7.6

```
pyenv  install --list | grep   3.7.2

v=3.7.2; cd ~/.pyenv; mkdir -pv cache; wget https://npm.taobao.org/mirrors/python/$v/Python-$v.tar.xz -P ~/.pyenv/cache/;pyenv install $v
```

4)配置数据库信息
```
mysql -uroot -p123456  -e "create database sso DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;"
mysql -uroot -p123456  -e "grant ALL PRIVILEGES on sso.* to root@'%' identified by '123456';"
mysql -uroot -p123456  -e "flush privileges;"
```

# 编写Dockerfile

```
mkdir /opt
```

5)dockerfile内容如下

vim /opt/Dockersso

```
FROM centos:7
ADD 3.7.2   /opt/python3
RUN echo 'export PATH=$PATH:/opt/python3/bin' > /etc/profile.d/python37.sh   
RUN curl -o /etc/pip.conf  https://client-doc.oss-cn-beijing.aliyuncs.com/pip.conf  
RUN source /etc/profile
ENV PATH /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/python3/bin
WORKDIR  /opt/sso
ADD sso  /opt/sso
RUN rm -f /etc/yum.repo.d/*repo  && \
    curl -o /etc/yum.repos.d/c7.repo   https://client-doc.oss-cn-beijing.aliyuncs.com/my-yumfile.repo && \ 
    yum install -y mariadb-libs mariadb-devel gcc net-tools && \
    python3 -m pip install -r /opt/sso/requirement.txt  && \
    python3  /opt/sso/manage.py makemigrations && \
    python3  /opt/sso/manage.py migrate 

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
```
6)# 切换到已经编译好的python目录,拉取SSO代码

```
cd ~/.pyenv/versions/
git clone https://github.com/iAutoAdmin/sso.git
```
- 修改SSO项目中数据库连接IP

  ```
 
  IPADD=`ip addr | grep inet | egrep -v '(127.0.0.1|inet6|docker)' | awk '{print $2}' | tr -d "addr:" | head -n 1 | cut -d / -f1`
  或者
   IPADD=`ifconfig eth0|grep 'inet '|awk  '{print $2}'`##以阿里云为例获取eth0的ip地址
  sed -i "s/127.0.0.1/$IPADD/g" /root/.pyenv/versions/sso/sso/settings.py         #替换项目连接数据库的ip地址
  ```

  ​                                       

7) # 构建docker 镜像
```
docker build -t dockersso -f /opt/Dockersso .
```
- # 测试启动容器

   #dockersso为构建的镜像名称，而ssov1为容器启动名称,本机的8000端口与容器中的8000端口做映射。
```
docker run -itd  --name=ssov1 -p8000:8000   dockersso       
```
# 进入容器测试

```
docker ps -a                       #查看容器启动状态
docker exec -it  ssov1  bash       #进入容器中

检查端口是否启动
netstat -lntup|grep 8000
```

8) 浏览器测试

```
访问172.17.119.254:8000  查看是否能到登录页面
```

诚谢
> 感谢大家对开源项目的支持。
