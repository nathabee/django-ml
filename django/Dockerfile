FROM python:3.12-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev ca-certificates && rm -rf /var/lib/apt/lists/*
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . .
FROM base AS dev
EXPOSE 8000
CMD ["bash","-lc","python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
FROM base AS prod
EXPOSE 8000
CMD ["gunicorn","config.wsgi:application","-b","0.0.0.0:8000","--workers","2"]
