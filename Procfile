web: cd webapp && python manage.py migrate && python manage.py loaddata data.json && python manage.py collectstatic --noinput && gunicorn webapp.wsgi