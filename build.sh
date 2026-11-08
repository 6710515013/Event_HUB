#!/usr/bin/env bash
# Render รันไฟล์นี้ทุกครั้งที่ deploy
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate