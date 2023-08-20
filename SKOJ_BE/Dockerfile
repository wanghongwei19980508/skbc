FROM python:3.8-alpine3.14

ENV OJ_ENV production

ADD . /app
WORKDIR /app

HEALTHCHECK --interval=5s --retries=3 CMD python3 /app/deploy/health_check.py

RUN echo `cat /dev/urandom | head -1 | md5sum | head -c 32` > /app/data/config/secret.key

RUN chmod +x /app/deploy/entrypoint.sh && \
    sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk add --update build-base nginx openssl curl unzip supervisor jpeg-dev zlib-dev postgresql-dev freetype-dev && \
    pip install -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com -r /app/requirements.txt && \
    apk del build-base --purge

ENTRYPOINT /app/deploy/entrypoint.sh