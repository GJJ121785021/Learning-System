## Learning-System


### 远程部署的过程
- mysql
    - 服务器搭建mysql并开放远程连接
    - 本地连远程数据库，生成数据表，创建user导入数据
- pip freeze > requirements.txt 导出依赖包
- 通过xftp将项目传到服务器，或者git clone(/偷笑)


```
第一次垃圾尝试
我的几个命令：
通过python:3.7构建容器：
docker run --name djangoproject -p 8000:8000 -it -d python:3.7 bash(这个bash这里应该是cmd，但是cmd后面再写试试)
复制项目：
docker cp /myproject(/LearningSystem) c2b05d841a19:/workspace
安装依赖：
pip install -i https://pypi.douban.com/simple -r requirements.txt
进入容器然后后台运行:
nohup python manage.py runserver 0.0.0.0:8000
关闭这个后台（杀相关进程？）
ps -aux | grep python|xargs kill -9
用Nginx设置反向代理
    # Nginx配置
    location / {
        # 方向代理转发地址
        proxy_pass http://127.0.0.1:8000
    }
  重新运行Nginx  nginx -s reload
  访问 Nginx的端口则可访问 -
用gunicorn运行：
gunicorn project.wsgi -b 0.0.0.0:8000 
运行是运行了，但是这个找不到静态资源，所以，这次简单的尝试先到这里
```




