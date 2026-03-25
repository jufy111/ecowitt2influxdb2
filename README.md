# GW2000 Weather Gateway → InfluxDB Logger

> Polls an **Ecowitt GW2000** gateway and writes sensor data (WS90, WH40, WH31, WH51, WH25) into **InfluxDB** [3].

---

## 📋 Overview

This project is a lightweight, Dockerized Python application that continuously polls an Ecowitt GW2000 weather gateway and logs sensor data into InfluxDB. It features timezone-aware UTC timestamps (Python 3.12+ safe), resilience to missing sensors and malformed packets, and batched writes to InfluxDB for efficiency [3].

---

## 🏗️ Project Structure

```
.
├── Dockerfile              # Python 3.12-slim container definition
├── docker-compose.yml      # Multi-service orchestration
├── ecowitt2influxDB.py     # Main application script
├── config.py               # ENV-based configuration loader
├── requirements.txt        # Python dependencies
├── .dockerignore           # Build context exclusions
└── .env                    # Environment variables (not committed)
```

---

## ⚙️ Configuration

All configuration is managed through **environment variables**, loaded in `config.py` [5]:

| Variable         | Description                        | Default                   |
|------------------|------------------------------------|---------------------------|
| `INFLUX_TOKEN`   | Authentication token for InfluxDB  | *(required)*              |
| `INFLUX_ORG`     | InfluxDB organization              | `default-org`             |
| `INFLUX_BUCKET`  | Target bucket for weather data     | `weather`                 |
| `INFLUX_URL`     | InfluxDB server URL                | `http://localhost:8086`   |
| `GW2000_IP`      | IP/hostname of the Ecowitt GW2000  | *(required)*              |
| `SAMPLE_TIME`    | Polling interval in seconds        | *(see config.py)*         |
| `LOCATION`       | Location tag for data points       | *(see config.py)*         |

Create a `.env` file in the project root (it is excluded from the Docker build context [1]):

```env
INFLUX_TOKEN=your-influxdb-token-here
INFLUX_ORG=my-org
INFLUX_BUCKET=weather
INFLUX_URL=http://influxdb:8086
GW2000_IP=192.168.1.100
SAMPLE_TIME=60
LOCATION=backyard
```

---

## 🐳 Docker

### Dockerfile

The image is built on **`python:3.12-slim`** and runs as a **non-root user** (`ecowitt`) for security [2]:

```dockerfile
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
# ============================================================
```

### Docker Compose

Use the following `docker-compose.yml` to run the logger alongside InfluxDB:

```yaml
version: "3.8"

services:
  # ──────────────────────────────────────────────
  # InfluxDB — Time-series database
  # ──────────────────────────────────────────────
  influxdb:
    image: influxdb:2
    container_name: influxdb
    restart: unless-stopped
    ports:
      - "8086:8086"
    volumes:
      - influxdb-data:/var/lib/influxdb2
      - influxdb-config:/etc/influxdb2
    environment:
      - DOCKER_INFLUXDB_INIT_MODE=setup
      - DOCKER_INFLUXDB_INIT_USERNAME=admin
      - DOCKER_INFLUXDB_INIT_PASSWORD=changeme123
      - DOCKER_INFLUXDB_INIT_ORG=${INFLUX_ORG:-default-org}
      - DOCKER_INFLUXDB_INIT_BUCKET=${INFLUX_BUCKET:-weather}
      - DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=${INFLUX_TOKEN}

  # ──────────────────────────────────────────────
  # Ecowitt GW2000 Logger
  # ──────────────────────────────────────────────
  ecowitt-logger:
    build: .
    container_name: ecowitt-logger
    restart: unless-stopped
    depends_on:
      - influxdb
    env_file:
      - .env
    environment:
      - INFLUX_URL=http://influxdb:8086

volumes:
  influxdb-data:
  influxdb-config:
```

---

## 🚀 Getting Started

### Option 1: Docker Compose (recommended)

```bash
# 1. Clone the repository
git clone https://github.com/your-user/gw2000-influxdb-logger.git
cd gw2000-influxdb-logger

# 2. Create your .env file
cp .env.example .env
# Edit .env with your values

# 3. Start all services
docker compose up -d

# 4. View logs
docker compose logs -f ecowitt-logger
```

### Option 2: Docker only (standalone)

```bash
# Build the image
docker build -t ecowitt2influxdb .

# Run the container
docker run -d \
  --name ecowitt-logger \
  --restart unless-stopped \
  --env-file .env \
  ecowitt2influxdb
```

---

## 📦 Dependencies

Defined in `requirements.txt` [4]:

| Package           | Purpose                          |
|-------------------|----------------------------------|
| `requests`        | HTTP calls to the GW2000 API     |
| `influxdb-client` | Write data points to InfluxDB    |

---

## 🛡️ .dockerignore

The following paths are excluded from the Docker build context to keep the image lean and secrets safe [1]:

```
__pycache__/
*.pyc
*.log
.git/
.env
```

---

## 🔍 Technical Details

- **Batched writes**: The InfluxDB write API is configured with a batch size of 1000 and a flush interval of 5000 ms for efficiency [3].
- **Non-root execution**: The container runs under the `ecowitt` user for improved security [2].
- **Unbuffered output**: `PYTHONUNBUFFERED=1` ensures real-time log visibility in `docker logs` [2].
- **UTC timestamps**: Uses Python 3.12+ `datetime.UTC` for timezone-aware timestamps [3].

---

## 📄 License

*(Add your license here)*
