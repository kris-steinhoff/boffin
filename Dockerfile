FROM python:3.12.4 as base
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
EXPOSE 8000

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.3
ENV PATH="/root/.local/bin:$PATH"
COPY pyproject.toml poetry.lock /tmp/
RUN poetry --directory=/tmp/ export --without-hashes -f requirements.txt -o /tmp/requirements-prod.txt

FROM base as dev
ENV SERVER_RELOAD=1
CMD ["poetry", "run", "python3", "boffin/main.py"]
RUN mkdir /app
WORKDIR /app
COPY --from=base /tmp/pyproject.toml /tmp/poetry.lock ./
RUN poetry install --with=dev --with=test
COPY . .
RUN poetry install

FROM python:3.12.4-slim as prod
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV SERVER_WORKERS=4
CMD ["python3", "boffin/main.py"]
RUN mkdir /app
WORKDIR /app
COPY --from=base /tmp/requirements-prod.txt ./
RUN pip install -r requirements-prod.txt
COPY . .
RUN pip install .
