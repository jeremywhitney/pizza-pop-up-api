#!/bin/bash

rm db.sqlite3
rm -rf ./pizzaapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations pizzaapi
python3 manage.py migrate pizzaapi
python3 manage.py migrate categories
python3 manage.py migrate payments
python3 manage.py migrate products
python3 manage.py migrate orders
python3 manage.py migrate orderproducts
python3 manage.py migrate pizzatoppings

