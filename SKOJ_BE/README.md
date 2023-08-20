# SKOJ Back End

[![django](https://img.shields.io/badge/django-3.2.9-blue.svg?style=flat-square)](https://github.com/django/django)
[![qrcode](https://img.shields.io/badge/qrcode-7.3.1-blue.svg?style=flat-square)](https://github.com/lincolnloop/python-qrcode)
[![redis](https://img.shields.io/badge/redis-3.5.3-blue.svg?style=flat-square)](https://github.com/redis/redis-py)
[![XlsxWriter](https://img.shields.io/badge/XlsxWriter-3.0.2-blue.svg?style=flat-square)](https://github.com/jmcnamara/XlsxWriter)

## Run Server

> 启动psql、redis、docker服务
> 将/data/config/secret.key进行生成

```bash
cat /dev/urandom | head -1 | md5sum | head -c 32
```

> 启动judge-server服务(保证10006端口空闲，且后端是8000端口)

```bash
docker-compose -f judge-server-deploy.yml up -d
```

> 启动后端服务

```bash
python manage.py makemigrations
python manage.py migrate
```

启动django shell界面

```bash
python manage.py shell
```

修改judgetoken
> from options.options import SysOptions; SysOptions.judge_server_token='6b506661f633965cafd0b72a3afa0fff'
> exit()

```bash
python manage.py runserver
```

## Deploy

```bash
mv docker-compose-deploy.yml ../docker-compose.yml
cd ..
docker-compose up -d
```
