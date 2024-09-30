# Use the official Python image as a base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Create a non-login user
RUN useradd --no-create-home --shell /bin/false appuser

# Set the working directory
WORKDIR /app

# Copy the Poetry files
COPY pyproject.toml poetry.lock* /app/

COPY app.py initdb.py /app/

# Install dependencies
RUN poetry install --no-root --no-dev && \
    python initdb.py &&  \
    mkdir public && \
    rm initdb.py && \
    chown -R appuser:appuser /app

# Switch to the non-login user
USER appuser

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD ["poetry", "run", "flask", "run", "--host=0.0.0.0"]
