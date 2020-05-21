FROM python:3.7

COPY . /app

# 选择工作文件夹
WORKDIR /app

# 安装包
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple/

EXPOSE 8000

CMD ["uwsgi", "/app/uwsgi.ini"]
