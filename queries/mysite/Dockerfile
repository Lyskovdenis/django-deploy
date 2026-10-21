FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Сначала копируем только requirements и ставим зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Затем копируем весь проект
COPY . .

# Для Django в Docker обычно используют gunicorn, но для учебной задачи
# можно оставить runserver
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]