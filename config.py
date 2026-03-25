import os

# -----------------------------------------------------------
# InfluxDB configuration
# -----------------------------------------------------------
token = os.getenv("INFLUX_TOKEN")
org = os.getenv("INFLUX_ORG", "default-org")
bucket = os.getenv("INFLUX_BUCKET", "weather")
influxDB_url = os.getenv("INFLUX_URL", "http://localhost:8086")

# -----------------------------------------------------------
# GW2000 / Ecowitt configuration
# -----------------------------------------------------------
GW2000_ip_address = os.getenv("GW2000_IP")

# -----------------------------------------------------------
# General application settings
# -----------------------------------------------------------
location = os.getenv("LOCATION", "weather_station")
sample_time = int(os.getenv("SAMPLE_TIME", "60"))

# -----------------------------------------------------------
# Basic validation (fail fast if critical vars missing)
# -----------------------------------------------------------
missing = []

if not token:
    missing.append("INFLUX_TOKEN")
if not GW2000_ip_address:
    missing.append("GW2000_IP")

if missing:
    raise RuntimeError(
        f"Missing required environment variables: {', '.join(missing)}"
    )
