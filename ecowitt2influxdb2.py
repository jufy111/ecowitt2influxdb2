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
        print()
        time.sleep(sample_time - time.monotonic() % sample_time)
        
def write_data(bucket, org, client, all_data_points, write_api):
    try:

        write_api.write(bucket=bucket, org=org, record=all_data_points)
        return
    except Exception as e:
        logging.error(f"Error writing data to InfluxDB: {e}")
        return

        
def getdata(GW2000_ip_address):
    try:
        response = requests.get('http://' + GW2000_ip_address + '/get_livedata_info?')
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
        data = response.json()
        return data
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
        return None  # Return None to indicate an error

def GW2000(data, bucket, org, location):
    try:

        data_points = [
            Point.measurement(location).tag('Measurement', 'GW2000').field('Temperature(C)',        float(data['wh25'][0]['intemp']))                   .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'GW2000').field('Humidity(%)',           float(data['wh25'][0]['inhumi'].replace("%", "")))  .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'GW2000').field('AbsolutePressure(hPa)', float(data['wh25'][0]['abs'].replace(" hPa", "")))  .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'GW2000').field('RelativePressure(hPa)', float(data['wh25'][0]['rel'].replace(" hPa", "")))  .time(datetime.utcnow(), WritePrecision.NS)
        ]

        return data_points
    
    except:
        print("GW2000 not avaliable")


# WS90 (Wittboy Multifunction Weather Station)
def WS90(data, bucket, org, location):
    try:
        data_points = [
            Point.measurement(location).tag('Measurement', 'WS90').field('Temperature(C)',          float(data['common_list'][0]['val']))                           .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('Humidity(%)',             float(data['common_list'][1]['val'].replace("%", "")))          .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('FeelsLike(C)',            float(data['common_list'][2]['val']))                           .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('DewPoint(C)',             float(data['common_list'][3]['val']))                           .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('WindChill(C)',            float(data['common_list'][4]['val']))                           .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('WindSpeed(km/h)',         3.6 * float(data['common_list'][5]['val'].replace(" m/s", ""))) .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('GustSpeed(km/h)',         3.6 * float(data['common_list'][6]['val'].replace(" m/s", ""))) .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('DayWindMax(km/h)',        3.6 * float(data['common_list'][7]['val'].replace(" m/s", ""))) .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('SolarRadiation(w/m2)',    float(data['common_list'][8]['val'].replace(" W/m2", "")))      .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('UVIndex',                 float(data['common_list'][9]['val']))                           .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('WindDirection',           float(data['common_list'][10]['val']))                          .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('RainEvent(mm)',           float(data['piezoRain'][0]['val'].replace(" mm", "")))          .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('RainRate(mm/h)',          float(data['piezoRain'][1]['val'].replace(" mm/Hr", "")))       .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('RainDay(mm)',             float(data['piezoRain'][2]['val'].replace(" mm", "")))          .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('RainWeek(mm)',            float(data['piezoRain'][3]['val'].replace(" mm", "")))          .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('RainMonth(mm)',           float(data['piezoRain'][4]['val'].replace(" mm", "")))          .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WS90').field('RainYear(mm)',            float(data['piezoRain'][5]['val'].replace(" mm", "")))          .time(datetime.utcnow(), WritePrecision.NS)            
        ]

        return data_points
    
    except: #error if cannot get data for WS90
        print("WARNING!...WS90 not avalaible")


def WH40(data, bucket, org, location):
    try:
        data_points = [
            Point.measurement(location).tag('Measurement', 'WH40').field('RainEvent(mm)',           float(data['rain'][0]['val'].replace(" mm", "")))          .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WH40').field('RainRate(mm/h)',          float(data['rain'][1]['val'].replace(" mm/Hr", "")))       .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WH40').field('RainDay(mm)',             float(data['rain'][2]['val'].replace(" mm", "")))          .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WH40').field('RainWeek(mm)',            float(data['rain'][3]['val'].replace(" mm", "")))          .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WH40').field('RainMonth(mm)',           float(data['rain'][4]['val'].replace(" mm", "")))          .time(datetime.utcnow(), WritePrecision.NS),
            Point.measurement(location).tag('Measurement', 'WH40').field('RainYear(mm)',            float(data['rain'][5]['val'].replace(" mm", "")))          .time(datetime.utcnow(), WritePrecision.NS) 
         
        ]

        return data_points


        print("WH40 posted to influxDB succsessfully")
    except:
        print("WH40-self emptying rain gauge not avalaible")
    

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
            print("WARNING!....No data from multi channel temperatures Sensors detected")
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
