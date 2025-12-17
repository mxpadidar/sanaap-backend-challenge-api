FROM python:3.13-slim-trixie

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_CACHE_DIR=/tmp/uv-cache
ENV UV_NO_DEV=1

RUN apt-get update \
  && apt-get install -y --no-install-recommends make libpq5 \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir uv \
  && uv sync --frozen --no-dev

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "make migrate && make rbac && make users && uv run --no-dev manage.py runserver 0.0.0.0:8000"]
