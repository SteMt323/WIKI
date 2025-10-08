#!/bin/bash
set -e

# instalar deps (Vercel ya usa requirements.txt en runtime, pero algunos ejemplos ejecutan aquí)
pip install -r requirements.txt

# migraciones opcional (ver advertencias más abajo)
python manage.py collectstatic --noinput
# Si quieres ejecutar migraciones en build (ver nota), podrías poner:
# python manage.py migrate --noinput
