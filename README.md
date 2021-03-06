﻿## Learning-System


### 远程部署的过程
- mysql
    - 服务器搭建mysql并开放远程连接
    - 本地连远程数据库，生成数据表，创建user导入数据
- pip freeze > requirements.txt 导出依赖包
- 通过xftp将项目传到服务器，或者git clone(/偷笑)


```
第一次垃圾尝试：
我的几个命令：
通过python:3.7构建容器：
docker run --name djangoproject -p 8000:8000 -it -d python:3.7 bash(这个bash这里应该是启动项目的cmd)
复制项目：
docker cp /myproject(/LearningSystem) c2b05d841a19:/workspace
安装依赖：
pip install -i https://pypi.douban.com/simple -r requirements.txt
进入容器然后后台运行:
nohup python manage.py runserver 0.0.0.0:8000
  关闭这个后台（杀相关进程？）1.ps -aux | grep python|xargs kill -9 (copy的，我看不懂)
    2.用杀进程的方法 ps -ef|grep runserver找到进程然后 kill
用Nginx设置反向代理
    # Nginx配置
    location / {
        # 反向代理转发地址
        proxy_pass http://127.0.0.1:8000
    }
  重新运行Nginx:  nginx -s reload
  访问 Nginx的端口则可访问 -
用gunicorn运行：
gunicorn project.wsgi -b 0.0.0.0:8000 (-w 8 指定工作进程,你一核的还指定个锤子 
--补充-还是指定为2吧，不然在ab测试时好像一个worker顶不住挂掉了后续的没跟上来导致请求超时测试失败)
后续再处理静态资源

第二次瞎操作：
不就是找静态资源吗
把静态资源/static 复制到Nginx容器中，我直接复制到了根目录下/static 我还复制了DRF的静态资源QAQ 在 根目录下/rest_framework
docker cp static 245e555f3ec6:/static
然后看我的静态资源配置①②
好吧直接看一下我Nginx里的部分配置：
server {
    listen       80;
    server_name  localhost;
    # 转发了host和ip
    proxy_set_header  Host  $http_host;
    proxy_set_header X-Forwarded-For  $remote_addr;

    root   /;
    #①
    location /static {
        alias /static;
    }
    #②
    location /static/rest_framework {
        alias /rest_framework;
    }
    # 这个是我个人的，我在html里加了/vue.js方便我的IDE，后来没有删，在这里直接禁止访问了，免得浪费时间
    location /vue.js {
        deny all;
    }
    # 转发地址(没使用docker的话host直接写127.0.0.1，我是在Linux上用了docker，连接到宿主机用的host一般是172.17.0.1（非Linux会有不同）)
    location / {
        proxy_pass http://172.17.0.1:8000;
    }
   
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
配置完 nginx -s reload一下应该就可以正常访问了


第三次一顿操作：
下面改用uWSGI web服务器来部署
Nginx和Gunicorn走的是http协议，直接通过 proxy_pass实现转发
Nginx和uWSGI走的是uwsgi协议，是通过 uwsgi_pass实现连接
将Nginx的配置改为：
server {
    listen       80;
    server_name  localhost;
       
    location / { 
        include  uwsgi_params;
        uwsgi_pass  172.17.0.1:8000;
    #    client_max_body_size 35m;
    }
    # 再重复一下上面①②的配置
}
重启一下nginx -s reload


额外说明：--- 配置负载均衡
在nginx配置的http{}内，server{}外 配置如下
upstream atom_server{
    ip_hash;
    server 10.112.13.45:8000;
    server 12.33.243.2:8000;
    server 183.21.78.89:8000 down;
    server 19.2.34.27:8000 weight=3;
    server 17.12.12.89:8000 backup;
    # fair;
}
# weight 负载权重
# down 当前server不参与负载均衡
# backup 当其他机器全挂了或满负荷时使用此服务
# ip_hash 按每个请求的hash结果分配
# fair 按后台响应时间分(第三方)

在server{}内 配置如下：
如果是转发http请求（gunicorn）：
location / {
    proxy_pass http://atom_server;
}
如果是转发是基于uwsgi协议：
location / {
    include  uwsgi_params;
    uwsgi_pass atom_server;
}


安装uwsgi ->  pip install uwsgi
然后到Django项目下加上文件uwsgi.ini配置文件
[uwsgi]
socket = 0.0.0.0:8000 
# 工作目录（项目目录）
chdir = /workspace2  
# wsgi.py 文件路径
wsgi-file = LearningSystem/wsgi.py 
processes = 1   
threads = 2  
enable-threads=true
# 主进程
master = true 
pidfile = /var/run/uwsgi.pid 
# 启动项目后，前台打印日志
# stats = 127.0.0.1:9191
# 启动项目后退出前台，日志输出到指定文件
# daemonize = /workspace2/uwsgi.log
# 启动项目后不退出前台，日志输出到指定文件
logto = /workspace2/uwsgi.log
# uwsgi只记录启动日志, 不记录request logging
# disable-logging = true

启动:uwsgi [--ini] uwsgi.ini
重启:uwsgi --reload /var/run/uwsgi.pid  #因为我配置了他的pid的路径，所以可以这样用
停止:uwsgi --stop /var/run/uwsgi.pid 


第四次收尾工作：
摸索着一步步部署成功后，下面改用Dockerfile的方式将项目直接部署
这里没有做Nginx和mysql的，因为个人感觉这两个第一次配置好了就得了，后续一般不会变动了
将uwsgi.ini和Dockerfile文件放在项目根目录下
↓↓Dockerfile↓↓
FROM python:3.7
COPY . /app
# 选择工作文件夹
WORKDIR /app
# 安装包
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple/
EXPOSE 8000
CMD ["uwsgi", "/app/uwsgi.ini"]

额外说明---uwsgi.ini不应该指定daemonize参数，否则启动项目后退出前台命令容器会认为自己没事情干了而自杀，你需要留一个前台在那一直挂着
可以配置logto参数它会把日志输出到指定文件但不会退出前台，个人认为指定stats参数最好，这样是将日志交给docker容器保管……（可以查看，限定，生命周期相同）

在项目根目录下执行 —>$ docker build -t imageName:Tag .
生成镜像后执行 ->$ docker run --name containerName -p 8000:8000 -d imageName:Tag
然后就可以看到容器在正常运行了

```




