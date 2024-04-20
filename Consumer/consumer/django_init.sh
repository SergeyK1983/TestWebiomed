#!/bin/sh

echo "=== Django start !!! ==="

echo "Django migrate ... "
python manage.py migrate

echo "Django collectstatic ... "
python manage.py collectstatic --no-input

echo "Django init_admin ... "
python manage.py initadmin

echo "Celery ... "
celery -A consumer worker -l INFO --detach
celery -A consumer beat -l INFO --detach

python /kafka_read/consumer.py &

echo "Run ... "
gunicorn consumer.wsgi:application --bind 0.0.0.0:9000
