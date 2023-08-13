# Weather Data Collection and InfluxDB Upload

This repository contains a Python script for collecting weather data from various sensors and uploading it to InfluxDB. The script retrieves data from different sources, processes it, and organizes it into InfluxDB-compatible data points. It's particularly designed to work with the following sensor types: GW2000, WS90 (Wittboy Multifunction Weather Station), WH40 (self-emptying rain gauge), WH31 (multi-channel temperature and humidity sensor), and WH51 (soil moisture sensor).

## Features

- Retrieves live weather data from GW2000, WS90, WH40, WH31, and WH51 sensors.
- Organizes the data into InfluxDB-compatible data points.
- Uses InfluxDBClient and WriteApi to upload the data to an InfluxDB instance.
- Supports the periodic collection and upload of data based on the specified time interval.
- Handles exceptions and logs errors for better debugging.

## Prerequisites

- Python 3.x
- `requests` library
- `influxdb` and `influxdb_client` libraries
- InfluxDB (2.0 + )instance (URL, token, organization, and bucket settings)
