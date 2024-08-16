#!/bin/bash
echo "Migrate"
python manage.py migrate --no-input
echo "=================================="
echo "Collect static files"
python manage.py collectstatic --no-input
echo "=================================="
echo "Prepopulate S3 bucket"
python /app/scripts/prepopulate_s3.py

if [ $# -eq 0 ]; then
  echo "=================================="
  echo "Start server"
  exec python manage.py runserver 0.0.0.0:8000
fi