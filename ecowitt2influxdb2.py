import requests
import time
from datetime import datetime

import influxdb.exceptions as inexc
from influxdb import InfluxDBClient
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import WriteOptions, SYNCHRONOUS
import logging


from config import token, org, bucket, influxDB_url, sample_time, GW2000_ip_address, location

# Create an empty list to accumulate data points for all sensors
all_data_points = []
client = InfluxDBClient(url=influxDB_url, token=token)
write_api = client.write_api(write_options=WriteOptions(batch_size=1000, flush_interval=5000))
logging.basicConfig(level=logging.ERROR) 

def main():
    
    while True:
        all_data_points = []
        print(str(datetime.now()))        
        data = getdata(GW2000_ip_address)


        all_data_points.extend(GW2000(data, bucket, org, location))
        all_data_points.extend(WS90(data, bucket, org, location))
        all_data_points.extend(WH40(data, bucket, org, location))
        all_data_points.extend(WH31(data, bucket, org, location))
        all_data_points.extend(WH51(data, bucket, org, location))

        write_data(bucket, org, client, all_data_points,write_api)
        time.sleep(sample_time - time.monotonic() % sample_time)

def write_data(bucket, org, client, all_data_points, write_api):
    try:

        write_api.write(bucket=bucket, org=org, record=all_data_points)
    except Exception as e:
        logging.error(f"Error writing data to InfluxDB: {e}")
    

        
def getdata(GW2000_ip_address):
    try:
        response = requests.get('http://' + GW2000_ip_address + '/get_livedata_info?')
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
        data = response.json()
        return data
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
        return None  # Return None to indicate an error



def extract_data_by_id(data, id_key):
    try:
        sensor_data = next(item for item in data if item.get('id') == id_key)
        return sensor_data.get('val')
    except StopIteration:
        return None
    except Exception as e:
        print(f"Error extracting data by ID {id_key}: {e}")
        return None


    

def GW2000(data, bucket, org, location):
    try:
        wh25_data = next(item for item in data['wh25'])
        data_points = [
            Point.measurement(location).tag('Measurement', 'GW2000').field('Temperature(C)', float(wh25_data.get('intemp').replace(" °C", ""))).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'GW2000').field('Humidity(%)', float(wh25_data.get('inhumi').replace("%", ""))).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'GW2000').field('AbsolutePressure(hPa)', float(wh25_data.get('abs').replace(" hPa", ""))).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'GW2000').field('RelativePressure(hPa)', float(wh25_data.get('rel').replace(" hPa", ""))).time(datetime.utcnow(), WritePrecision.NS)
        ]
        return data_points
    except:
        print("GW2000 not available")




# WS90 (Wittboy Multifunction Weather Station)
def WS90(data, bucket, org, location):

    try:
        common_list_data = data['common_list']
        temperature = extract_data_by_id(common_list_data, "0x02")
        humidity = extract_data_by_id(common_list_data, "0x07")
        feels_like = extract_data_by_id(common_list_data, "3")
        heat_index = extract_data_by_id(common_list_data, "0x05")
        dew_point = extract_data_by_id(common_list_data, "0x03")      
        wind_chill = extract_data_by_id(common_list_data, "0x04")
        wind_speed = extract_data_by_id(common_list_data, "0x0B")
        gust_speed = extract_data_by_id(common_list_data, "0x0C")
        day_wind_max = extract_data_by_id(common_list_data, "0x19")        
        solar_radiation = extract_data_by_id(common_list_data, "0x15")
        uv_index = extract_data_by_id(common_list_data, "0x17")
        wind_direction = extract_data_by_id(common_list_data, "0x0A")
        rain_event = extract_data_by_id(data['rain'], "0x0D") 
        rain_rate = extract_data_by_id(data['rain'], "0x0E")
        rain_day = extract_data_by_id(data['rain'], "0x10")
        rain_week = extract_data_by_id(data['rain'], "0x11")
        rain_month = extract_data_by_id(data['rain'], "0x12")
        rain_year = extract_data_by_id(data['rain'], "0x13")

        
        data_points = [
            Point.measurement(location).tag('Measurement', 'WS90').field('Temperature(C)', float(temperature)).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('Humidity(%)', float(humidity.replace("%", ""))).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('FeelsLike(C)', float(feels_like)).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('HeatIndex(C)', float(heat_index)).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('DewPoint(C)', float(dew_point)).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('WindChill(C)', float(wind_chill)).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('WindSpeed(km/h)', float(wind_speed.replace(" m/s", "")) * 3.6).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('GustSpeed(km/h)', float(gust_speed.replace(" m/s", "")) * 3.6).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('DayWindMax(km/h)', float(day_wind_max.replace(" m/s", "")) * 3.6).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('SolarRadiation(w/m2)', float(solar_radiation.replace(" W/m2", ""))).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('UVIndex', float(uv_index)).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('WindDirection', float(wind_direction)).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('RainEvent(mm)', float(rain_event.replace(" mm", ""))).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('RainRate(mm/h)', float(rain_rate.replace(" mm/Hr", ""))).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('RainDay(mm)', float(rain_day.replace(" mm", ""))).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('RainWeek(mm)', float(rain_week.replace(" mm", ""))).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('RainMonth(mm)', float(rain_month.replace(" mm", ""))).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('RainYear(mm)', float(rain_year.replace(" mm", ""))).time(datetime.utcnow(), WritePrecision.NS)
        ]

        return data_points
    except Exception as e:
        logging.error(f"Error in WS90 function: {e}")
        return []



def WH40(data, bucket, org, location):
    try:
        rain_event = extract_data_by_id(data['rain'], "0x0D")
        rain_rate = extract_data_by_id(data['rain'], "0x0E")
        rain_day = extract_data_by_id(data['rain'], "0x10")
        rain_week = extract_data_by_id(data['rain'], "0x11")
        rain_month = extract_data_by_id(data['rain'], "0x12")
        rain_year = extract_data_by_id(data['rain'], "0x13")

        # Check for None values and handle them appropriately
        if any(value is None for value in [rain_event, rain_rate, rain_day, rain_week, rain_month, rain_year]):
            print("WARNING! Some data points in WH40 are not available.")
            return []

        data_points = [
            Point.measurement(location).tag('Measurement', 'WH40').field('RainEvent(mm)', float(rain_event.replace(" mm", ""))).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WH40').field('RainRate(mm/h)', float(rain_rate.replace(" mm/Hr", ""))).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WH40').field('RainDay(mm)', float(rain_day.replace(" mm", ""))).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WH40').field('RainWeek(mm)', float(rain_week.replace(" mm", ""))).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WH40').field('RainMonth(mm)', float(rain_month.replace(" mm", ""))).time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WH40').field('RainYear(mm)', float(rain_year.replace(" mm", ""))).time(datetime.utcnow(), WritePrecision.NS)
        ]

        return data_points
    except Exception as e:
        logging.error(f"Error in WH40 function: {e}")
        return []

    

def WH31(data, bucket, org, location):
    data_sum=[]
    for i,a in enumerate(data['ch_aisle']):
        try:
            data_points = [
                Point.measurement(location).tag('Measurement', 'WH31_channel_'+ data['ch_aisle'][i]['channel']).field('Temperature(C)', float(data['ch_aisle'][i]['temp'])).time(datetime.utcnow(), WritePrecision.NS),
                Point.measurement(location).tag('Measurement', 'WH31_channel_'+ data['ch_aisle'][i]['channel']).field('Humidity(%)', float(data['ch_aisle'][i]['humidity'].replace("%", ""))).time(datetime.utcnow(), WritePrecision.NS)             
            ]
            data_sum.extend(data_points)
            data_points = []
        except:
            logging.error(f"WARNING!....No data from multi channel temperatures Sensors detected: {e}")
    return data_sum   
    print("WH31(s) posted to influxDB succsessfully")   

def WH51(data, bucket, org, location):
    data_sum2=[]
    for i,a in enumerate(data['ch_soil']):
        try:
            data_points = [
                Point.measurement(location).tag('Measurement', 'WH51_channel_'+ data['ch_soil'][i]['channel']).field('Moisture(%)',float(data['ch_soil'][i]['humidity'].replace("%", ""))).time(datetime.utcnow(), WritePrecision.NS)     
            ]
            data_sum2.extend(data_points)
            data_points = []
            
        except:
            print("WARNING: No data from soil moisure Sensor WH51_Channel_"+data['ch_soil'][i]['channel']+" detected")
    return data_sum2       
    print("WH51(s) posted to influxDB succsessfully") 


if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("Program stopped by keyboard interrupt [CTRL_C] by user.")
            break
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            time.sleep(sample_time)
