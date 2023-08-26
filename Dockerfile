FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y gcc libpq-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY webapp /app/
CMD ["gunicorn", "manage.wsgi:application", "--bind", "0.0.0.0:80"]
