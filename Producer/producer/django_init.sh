#!/bin/sh

echo "=== Django start !!! ==="

echo "Django migrate ... "
python manage.py migrate

echo "Django collectstatic ... "
python manage.py collectstatic --no-input

echo "Django init_admin ... "
python manage.py initadmin

echo "Run ... "
gunicorn producer.wsgi:application --bind 0.0.0.0:8000
