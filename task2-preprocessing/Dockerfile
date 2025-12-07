# Use Python base image
FROM python:3.10-slim

WORKDIR /app

# --- Install system dependencies for matplotlib & scientific packages ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libfreetype6-dev \
    libpng-dev \
    pkg-config \
    libopenblas-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# --- Copy requirements and install Python dependencies ---
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# --- Copy your source code ---
COPY preprocess.py .

CMD ["python", "preprocess.py"]

