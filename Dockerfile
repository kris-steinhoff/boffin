FROM python:3.12-slim
EXPOSE 80


RUN groupadd -g 5000 app && useradd -k HOME_MODE=0755 -d /app -m -u 5000 -g 5000 app
RUN apt-get update && apt-get install -y --no-install-recommends \
    tini \
    && rm -rf /var/lib/apt/lists/*
RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR='/tmp/poetry_cache' \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app
USER app

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

COPY . .
RUN poetry install

ENTRYPOINT ["/bin/tini", "--"]
CMD ["uvicorn", "boffin.main:app", "--host=0.0.0.0", "--port=80", "--no-access-log", "--use-colors"]
