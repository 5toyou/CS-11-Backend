FROM python:3.10-slim


RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


RUN python manage.py collectstatic --noinput

EXPOSE 8000

#CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:10000"]
CMD ["sh", "-c", "python manage.py migrate && python create_admin.py && python manage.py runserver 0.0.0.0:10000"]