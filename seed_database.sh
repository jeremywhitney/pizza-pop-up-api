#!/bin/bash

rm db.sqlite3
rm -rf ./pizzaapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations pizzaapi
python3 manage.py migrate pizzaapi
python3 manage.py loaddata categories

