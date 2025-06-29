#!/bin/bash

echo "Waiting for MySQL to be ready..."
until mysql -h mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "SELECT 1" > /dev/null 2>&1; do
    echo "Waiting for MySQL..."
    sleep 2
done

DATABASE_EXISTS=$(mysql -h mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "SHOW DATABASES LIKE 'dphish_db';" | grep 'dphish_db' || true)
if [ -z "$DATABASE_EXISTS" ]; then
    echo "Creating database dphish_db..."
    mysql -h mysql -u root -p"${MYSQL_ROOT_PASSWORD}" -e "CREATE DATABASE dphish_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
else
    echo "Database dphish_db already exists."
fi

python manage.py migrate --noinput

exec daphne -b 0.0.0.0 -p 7000 project.asgi:application
