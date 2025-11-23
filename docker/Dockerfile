from python:3.13-alpine


ENV TZ=Europe/Moscow

RUN apk add --no-cache bash

RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/* /usr/share/man/*


WORKDIR /app

COPY ./project/. /app

COPY pyproject.toml /app
COPY uv.lock /app


ENV UV_PROJECT_ENVIRONMENT=/.venv

RUN pip install uv
RUN uv sync --frozen
RUN uv add uvicorn

EXPOSE 8000

