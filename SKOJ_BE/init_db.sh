#! /bin/bash
set -x

if [[ ! -f manage.py ]]; then
    echo "No manage.py, wrong location"
    exit 1
fi

sleep 2
docker rm -f oj-postgres-dev oj-redis-dev
docker run -it -d -e POSTGRES_DB=skojda -e POSTGRES_USER=skoj -e POSTGRES_PASSWORD=Nice_try -p 127.0.0.1:5432:5432 --name oj-postgres-dev postgres:10-alpine
docker run -it -d -p 127.0.0.1:6380:6379 --name oj-redis-dev redis:4.0-alpine

if [ "$1" = "--migrate" ]; then
    sleep 3
    echo `cat /dev/urandom | head -1 | md5sum | head -c 32` > data/config/secret.key
    python manage.py migrate
    python manage.py inituser --username root --password rootroot --action create_super_admin
fi