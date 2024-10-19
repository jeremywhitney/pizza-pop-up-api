#!/bin/bash

rm db.sqlite3
rm -rf ./pizzaapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations pizzaapi
python3 manage.py migrate pizzaapi
python3 manage.py loaddata categories
python3 manage.py loaddata payments
python3 manage.py loaddata products
python3 manage.py loaddata orders
python3 manage.py loaddata orderproducts
python3 manage.py loaddata pizzatoppings

