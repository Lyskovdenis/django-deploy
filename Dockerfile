FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    DJANGO_SETTINGS_MODULE=mysite.settings

WORKDIR /app

RUN pip install --no-cache-dir poetry==2.5.1

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root

COPY . .

WORKDIR /app/mysite

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && gunicorn mysite.wsgi:application --bind 0.0.0.0:8000"]