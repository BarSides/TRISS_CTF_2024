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
    mkdir /app/templates && \
    mkdir /app/static

COPY . /app/

RUN poetry config virtualenvs.create false && \
    poetry install --no-root

EXPOSE 8002

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8002", "app:app"]