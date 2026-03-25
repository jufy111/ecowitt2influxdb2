# ============================================================
# Ecowitt GW2000 → InfluxDB Logger (ENV-based)
# ============================================================

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ecowitt2influxDB.py .
COPY config.py .

RUN useradd -m ecowitt
USER ecowitt

CMD ["python", "ecowitt2influxDB.py"]
