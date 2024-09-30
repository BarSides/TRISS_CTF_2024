# Use the official Python image as a base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt update &&  \
    apt upgrade &&  \
    pip install --upgrade pip &&  \
    pip install poetry gunicorn[gevent] && \
    mkdir /app/templates

COPY templates/*.html /app/templates/
COPY recursive_py/solveme.py app.py initdb.py /app/

COPY pyproject.toml poetry.lock /app/
# Install dependencies.  WORKDIR does not work for some reason
RUN poetry config virtualenvs.create false &&  \
    poetry install --no-root
    # chown -R appuser:appuser /app && \

COPY entrypoint.sh /app/
RUN mkdir public && \
    chmod 500 ./entrypoint.sh

# Expose the port the app runs on
EXPOSE 5000

ENTRYPOINT "/app/entrypoint.sh"