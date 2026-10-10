
#!/bin/sh
set -e

if [ "$#" -gt 0 ]; then
    exec "$@"
fi

echo "==> Executando makemigrations..."
python manage.py makemigrations

echo "==> Executando migrate..."
python manage.py migrate

echo "==> Executando seed_items..."
python manage.py seed_items

echo "==> Executando seed_models..."
python manage.py seed_models

echo "==> Verificando superusuário..."
python manage.py shell -c '
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ["DJANGO_SUPERUSER_USERNAME"]

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(
        username=username,
        email=os.environ["DJANGO_SUPERUSER_EMAIL"],
        password=os.environ["DJANGO_SUPERUSER_PASSWORD"],
    )
    print("Superusuário criado.")
else:
    print("Superusuário já existe.")
'

echo "==> Iniciando Daphne..."
exec daphne -b 0.0.0.0 -p 8000 core.asgi:application
