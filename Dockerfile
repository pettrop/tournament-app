# Výber základného obrazu s Python 3.8
FROM python:3.8

# Nastavenie pracovného adresára v kontajneri
WORKDIR /app

# Kopírovanie obsahu aktuálneho adresára (vaša aplikácia) do kontajnera
ADD ./ /app/

# Inštalácia potrebných závislostí
RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y gcc libpq-dev
RUN pip install -r requirements.txt

# Vytvorenie adresára pre statické súbory a zhromaždenie týchto súborov
RUN mkdir -p /app/staticfiles
RUN python webapp/manage.py collectstatic --noinput

# Spustenie aplikácie cez Gunicorn
CMD ["gunicorn", "webapp.webapp.wsgi:application", "--bind", "0.0.0.0:80"]