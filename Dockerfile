FROM python:3.12.4 as base
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
EXPOSE 8000

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.3
ENV PATH="/root/.local/bin:$PATH"
COPY pyproject.toml poetry.lock /tmp/
RUN poetry --directory=/tmp/ export --without-hashes -f requirements.txt -o /tmp/requirements-prod.txt

FROM base as dev
CMD ["poetry", "run", "fastapi", "dev", "boffin/main.py", "--host=0.0.0.0", "--port=8000", "--app=app"]
RUN mkdir /app
WORKDIR /app
COPY --from=base /tmp/pyproject.toml /tmp/poetry.lock ./
RUN poetry install --with=dev --with=test
COPY . .

ENV DATABASE_URL="sqlite:///db.sqlite3"

FROM python:3.12.4-slim as prod
CMD ["fastapi", "run", "boffin/main.py", "--app=app"]
RUN mkdir /app
WORKDIR /app
COPY --from=base /tmp/requirements-prod.txt ./
RUN pip install -r requirements-prod.txt

COPY . .
