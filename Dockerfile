FROM python:3.12.3-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create app directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    python3.12-venv \
    curl \
    && apt-get clean

# Create virtual environment
RUN python3 -m venv /opt/venv

# Activate virtualenv for all future RUN and CMD
ENV PATH="/var/lib/jenkins/workspace/CMS/venv/bin:$PATH"

# Install Python packages
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/
