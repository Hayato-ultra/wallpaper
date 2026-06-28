#!/bin/bash
pip install -r requirements.txt
npm ci --production=false --ignore-scripts
npm run build:css
python manage.py migrate --noinput
python manage.py collectstatic --noinput
