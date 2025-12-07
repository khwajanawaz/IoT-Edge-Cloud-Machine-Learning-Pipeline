FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libfreetype6-dev libpng-dev pkg-config gfortran git \
 && pip install --no-cache-dir -r requirements.txt \
 && rm -rf /var/lib/apt/lists/*

# Download ML Engine inside container
RUN git clone https://github.com/ncl-iot-team/CSC8112_MLEngine.git /app/CSC8112_MLEngine

COPY predictor.py .

CMD ["python", "predictor.py"]

