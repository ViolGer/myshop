FROM python:3.12-alpine

WORKDIR /code
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN apk add --no-cache build-base postgresql-dev zlib-dev jpeg-dev

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-root

COPY . .

EXPOSE 8000
