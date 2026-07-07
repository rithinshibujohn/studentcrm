#!/usr/bin/env bash

set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --noinput

python manage.py migrate

python manage.py shell <<EOF
from django.contrib.auth.models import User

username = "admin"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email="admin@example.com",
        password="Admin@123"
    )
    print("Superuser created.")
else:
    print("Superuser already exists.")
EOF