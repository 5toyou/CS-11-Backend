# Використовуємо офіційний легкий образ Python
FROM python:3.11-slim

# Встановлюємо змінні оточення, щоб Python не буферизував вивід і не писав .pyc файли
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Створюємо робочу директорію в контейнері
WORKDIR /app

# Встановлюємо системні залежності, необхідні для компіляції деяких пакетів (наприклад, psycopg2 для Postgres)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копіюємо файл залежностей та встановлюємо їх
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код проєкту в контейнер
COPY . /app/