#!/bin/bash

python ./source/manage.py collectstatic --noinput

# i commit my migration files to git so i dont need to run it on server
python ./source/manage.py migrate

python ./source/manage.py update_translation_fields

# here it start nginx and the uwsgi
gunicorn -w 3 --chdir ./source quantum.wsgi --bind 0.0.0.0:8000