#!/usr/bin/env python3
"""
============================================================
 GW2000 Weather Gateway → InfluxDB Logger
------------------------------------------------------------
 Author: You
 Description:
   Polls an Ecowitt GW2000 gateway and writes sensor data
   (WS90, WH40, WH31, WH51, WH25) into InfluxDB.

 Notes:
   - Uses timezone-aware UTC timestamps (Python 3.12+ safe)
   - Resilient to missing sensors and malformed packets
   - Batched writes to InfluxDB for efficiency
============================================================
"""

import time
import logging
import requests
from datetime import datetime, UTC

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import WriteOptions

from config import (
    token,
    org,
    bucket,
    influxDB_url,
    sample_time,
    GW2000_ip_address,
    location,
)

# -----------------------------------------------------------
# Logging configuration
# -----------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# -----------------------------------------------------------
# InfluxDB client setup
# -----------------------------------------------------------
client = InfluxDBClient(url=influxDB_url, token=token)
write_api = client.write_api(
    write_options=WriteOptions(batch_size=1000, flush_interval=5000)
)

# -----------------------------------------------------------
# Helper functions
# -----------------------------------------------------------
def utcnow():
    """Return timezone-aware UTC datetime."""
    return datetime.now(UTC)


def safe_float(value, unit=None):
    """
    Convert a string value to float, stripping optional units.
    Returns None if conversion fails.
    """
    try:
        if value is None:
            return None
        if unit:
            value = value.replace(unit, "")
        return float(value.strip())
    except Exception:
        return None


def extract_data_by_id(data_list, id_key):
    """
    Safely extract a 'val' from a list of dicts using an ID.
    """
    if not isinstance(data_list, list):
        return None
    for item in data_list:
        if item.get("id") == id_key:
            return item.get("val")
    return None


def getdata(gateway_ip):
    """
    Fetch live data from GW2000 gateway.
    """
    try:
        url = f"http://{gateway_ip}/get_livedata_info?"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logging.error(f"Failed to fetch data from GW2000: {e}")
        return None


def write_data(points):
    """
    Write accumulated points to InfluxDB.
    """
    if not points:
        logging.warning("No data points to write")
        return
    try:
        write_api.write(bucket=bucket, org=org, record=points)
    except Exception as e:
        logging.error(f"InfluxDB write failed: {e}")

# -----------------------------------------------------------
# Sensor handlers
# -----------------------------------------------------------
def GW2000(data):
    """Indoor WH25 sensor via GW2000."""
    try:
        wh25 = data.get("wh25", [{}])[0]
        now = utcnow()

        return [
            Point.measurement(location)
                .tag("Measurement", "GW2000")
                .field("Temperature(C)", safe_float(wh25.get("intemp")))
                .field("Humidity(%)", safe_float(wh25.get("inhumi"), "%"))
                .field("AbsolutePressure(hPa)", safe_float(wh25.get("abs"), " hPa"))
                .field("RelativePressure(hPa)", safe_float(wh25.get("rel"), " hPa"))
                .time(now, WritePrecision.NS)
        ]
    except Exception as e:
        logging.error(f"GW2000 error: {e}")
        return []


def WS90(data):
    """WS90 Wittboy multifunction sensor."""
    try:
        common = data.get("common_list", [])
        rain = data.get("piezoRain", [])
        now = utcnow()

        return [
            Point.measurement(location)
                .tag("Measurement", "WS90")
                .field("Temperature(C)", safe_float(extract_data_by_id(common, "0x02")))
                .field("Humidity(%)", safe_float(extract_data_by_id(common, "0x07"), "%"))
                .field("FeelsLike(C)", safe_float(extract_data_by_id(common, "3")))
                .field("HeatIndex(kPa)", safe_float(extract_data_by_id(common, "5"), " kPa"))
                .field("DewPoint(C)", safe_float(extract_data_by_id(common, "0x03")))
                .field("WindSpeed(km/h)", safe_float(extract_data_by_id(common, "0x0B"), " m/s") * 3.6)
                .field("GustSpeed(km/h)", safe_float(extract_data_by_id(common, "0x0C"), " m/s") * 3.6)
                .field("DayWindMax(km/h)", safe_float(extract_data_by_id(common, "0x19"), " m/s") * 3.6)
                .field("SolarRadiation(W/m2)", safe_float(extract_data_by_id(common, "0x15"), " W/m2"))
                .field("UVIndex", safe_float(extract_data_by_id(common, "0x17")))
                .field("WindDirection(deg)", safe_float(extract_data_by_id(common, "0x0A")))
                .field("RainEvent(mm)", safe_float(extract_data_by_id(rain, "0x0D"), " mm"))
                .field("RainRate(mm/h)", safe_float(extract_data_by_id(rain, "0x0E"), " mm/Hr"))
                .field("RainDay(mm)", safe_float(extract_data_by_id(rain, "0x10"), " mm"))
                .field("RainWeek(mm)", safe_float(extract_data_by_id(rain, "0x11"), " mm"))
                .field("RainMonth(mm)", safe_float(extract_data_by_id(rain, "0x12"), " mm"))
                .field("RainYear(mm)", safe_float(extract_data_by_id(rain, "0x13"), " mm"))
                .time(now, WritePrecision.NS)
        ]
    except Exception as e:
        logging.error(f"WS90 error: {e}")
        return []


def WH40(data):
    """Traditional rain gauge."""
    try:
        rain = data.get("rain", [])
        now = utcnow()

        return [
            Point.measurement(location)
                .tag("Measurement", "WH40")
                .field("RainEvent(mm)", safe_float(extract_data_by_id(rain, "0x0D"), " mm"))
                .field("RainRate(mm/h)", safe_float(extract_data_by_id(rain, "0x0E"), " mm/Hr"))
                .field("RainDay(mm)", safe_float(extract_data_by_id(rain, "0x10"), " mm"))
                .field("RainWeek(mm)", safe_float(extract_data_by_id(rain, "0x11"), " mm"))
                .field("RainMonth(mm)", safe_float(extract_data_by_id(rain, "0x12"), " mm"))
                .field("RainYear(mm)", safe_float(extract_data_by_id(rain, "0x13"), " mm"))
                .time(now, WritePrecision.NS)
        ]
    except Exception as e:
        logging.error(f"WH40 error: {e}")
        return []


def WH31(data):
    """Multi-channel temperature/humidity sensors."""
    points = []
    for ch in data.get("ch_aisle", []):
        try:
            points.append(
                Point.measurement(location)
                    .tag("Measurement", f"WH31_channel_{ch.get('channel')}")
                    .field("Temperature(C)", safe_float(ch.get("temp")))
                    .field("Humidity(%)", safe_float(ch.get("humidity"), "%"))
                    .time(utcnow(), WritePrecision.NS)
            )
        except Exception as e:
            logging.warning(f"WH31 channel error: {e}")
    return points


def WH51(data):
    """Soil moisture sensors."""
    points = []
    for ch in data.get("ch_soil", []):
        try:
            points.append(
                Point.measurement(location)
                    .tag("Measurement", f"WH51_channel_{ch.get('channel')}")
                    .field("Moisture(%)", safe_float(ch.get("humidity"), "%"))
                    .time(utcnow(), WritePrecision.NS)
            )
        except Exception as e:
            logging.warning(f"WH51 channel error: {e}")
    return points

# -----------------------------------------------------------
# Main loop
# -----------------------------------------------------------
def main():
    logging.info("GW2000 → InfluxDB logger started")

    while True:
        start = time.monotonic()
        data = getdata(GW2000_ip_address)

        if data:
            points = []
            points.extend(GW2000(data))
            points.extend(WS90(data))
            points.extend(WH40(data))
            points.extend(WH31(data))
            points.extend(WH51(data))
            write_data(points)

        # Align loop to sample_time
        sleep_time = max(0, sample_time - (time.monotonic() - start))
        time.sleep(sleep_time)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Program stopped by user (CTRL+C)")
    except Exception as e:
        logging.critical(f"Fatal error: {e}")
