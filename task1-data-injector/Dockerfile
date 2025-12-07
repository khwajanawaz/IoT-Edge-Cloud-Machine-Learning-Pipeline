# -------------------------------
# Dockerfile – Task 1 Data Injector
# -------------------------------

# Use a small Python base image
FROM python:3.10-slim

# Create work directory inside container
WORKDIR /app

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script
COPY injector.py .

# Expose MQTT port (optional for visibility)
EXPOSE 1883

# Default command
CMD ["python", "injector.py"]

