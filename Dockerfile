FROM python:3.12.3-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    python3.12-venv \
    && apt-get clean

# Create virtual environment in standard location
RUN python3 -m venv /opt/venv

# Use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Install Python packages inside virtualenv
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the Django project into the container
COPY . /app/
