#!/bin/bash

rm db.sqlite3
rm -rf ./pizzaapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations pizzaapi
python3 manage.py migrate pizzaapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata profiles
python3 manage.py loaddata employee_profiles
python3 manage.py loaddata categories
python3 manage.py loaddata payments
python3 manage.py loaddata products
python3 manage.py loaddata orders
python3 manage.py loaddata order_products
python3 manage.py loaddata pizza_toppings
