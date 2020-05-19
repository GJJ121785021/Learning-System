## Learning-System


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
docker run --name djangoproject -p 8000:8000 -it -d python:3.7 bash(这个bash这里应该是cmd，但是cmd后面再写试试)
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
gunicorn project.wsgi -b 0.0.0.0:8000 (-w 8 指定工作进程,你一核的还指定个锤子)
运行是运行了，但是这个找不到静态资源，所以，这次简单的尝试先到这里

第二次瞎操作：
不就是找静态资源吗
把静态资源/static 复制到Nginx容器中，我直接复制到了根目录下/static 我还复制了DRF的静态资源QAQ 在 根目录下/rest_framework
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
    # 转发地址(正确操作应该是转发到docker外的宿主机的端口吧，但是我8太会)
    location / {
        proxy_pass http://120.78.175.96:8000;
    }
   
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
配置完nginx -s reload一下应该就可以正常访问了


第三次一顿操作：


```




