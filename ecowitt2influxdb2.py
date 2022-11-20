
## Validated on GW2000 firmware V2.1.8

Requiered Python Dependencies
#pip install influxdb
#pip install influxdb_client
#pip install wmi



####################################################################################################
# Import modules
####################################################################################################

import requests
#import json
import time
from datetime import datetime

import influxdb.exceptions as inexc
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS



####################################################################################################
# InfluxDB (V2) Database Details
####################################################################################################
token = "O9DKz7dpSsz_TueaSdnUlTwOGjctsUO8X4nK8jy_8pWx6run4m0D1gFQtv4ZssW7WUaw7hUJ64dfAfaS58dlfw=="  #example token
org = "yourorg"
bucket = "ecowitt"  #what you set your bucket as
influxDB_url = "http://192.168.0.0:8086"  # ip address of influxDB server

####################################################################################################
# EcoWitt devices details
####################################################################################################
sample_time = 10 # in seconds
GW2000_ip_address = '192.168.0.0'
location = 'home'   #a unique identifier for location


# GW2000 Basestation
####################################################################################################
def GW2000():
    try:
        Sensor_GW2000_indoortemp=     location + ",Measurement=GW2000" +  " Temperature(C)="        +   str(data['wh25'][0]['intemp'])
        Sensor_GW2000_indoorhumid=    location + ",Measurement=GW2000" +  " Humidity(%)="           +   str(data['wh25'][0]['inhumi'].replace("%", ""))
        Sensor_GW2000_abspressure=    location + ",Measurement=GW2000" +  " AbsolutePressure(hPa)=" +   str(data['wh25'][0]['abs'].replace(" hPa", ""))
        Sensor_GW2000_relpressure=    location + ",Measurement=GW2000" +  " RelativePressure(hPa)=" +   str(data['wh25'][0]['rel'].replace(" hPa", ""))

        try:     
            write_api.write(bucket, org, Sensor_GW2000_indoortemp)
            write_api.write(bucket, org, Sensor_GW2000_indoorhumid)
            write_api.write(bucket, org, Sensor_GW2000_abspressure)
            write_api.write(bucket, org, Sensor_GW2000_relpressure)

        except:
            print("error writing GW2000 data to influxDB")
            
        print("GW2000 posted to influxDB succsessfully")
        
    except:
        print("GW2000 not avaliable")



# WS90 (Wittboy Multifunction Weather Station)
####################################################################################################
def WS90():
    try:
        #imports data from json, format it so that influxDB can read it
        Sensor_WS90_Temp=       location + ",Measurement=WS90" +  " Temperature(C)="        +str(data['common_list'][0]['val'])
        Sensor_WS90_Humid=      location + ",Measurement=WS90" +  " Humidity(%)="           +str(data['common_list'][1]['val'].replace("%", ""))
        Sensor_WS90_FeelLike=   location + ",Measurement=WS90" +  " FeelsLike(C)="          +str(data['common_list'][2]['val'])
        Sensor_WS90_DewPoint=   location + ",Measurement=WS90" +  " DewPoint(C)="           +str(data['common_list'][3]['val'])
        Sensor_WS90_WindChill=  location + ",Measurement=WS90" +  " WindChill(C)="          +str(data['common_list'][4]['val'])
        Sensor_WS90_WindSpeed=  location + ",Measurement=WS90" +  " WindSpeed(km/h)="       +str(3.6 * float(data['common_list'][5]['val'].replace(" m/s", "")))
        Sensor_WS90_GustSpeed=  location + ",Measurement=WS90" +  " GustSpeed(km/h)="       +str(3.6 * float(data['common_list'][6]['val'].replace(" m/s", "")))
        Sensor_WS90_DayWindMax= location + ",Measurement=WS90" +  " DayWindMax(km/h)="      +str(3.6 * float(data['common_list'][7]['val'].replace(" m/s", "")))
        Sensor_WS90_Solar=      location + ",Measurement=WS90" +  " SolarRadiation(w/m2)="  +str(data['common_list'][8]['val'].replace(" W/m2", ""))
        Sensor_WS90_UVIndex=    location + ",Measurement=WS90" +  " UVIndex="               +str(data['common_list'][9]['val'])
        Sensor_WS90_WindDir=    location + ",Measurement=WS90" +  " WindDirection="         +str(data['common_list'][10]['val'])
        Sensor_WS90_rainEvent=  location + ",Measurement=WS90" +  " RainEvent(mm)="         +str(data['piezoRain'][0]['val'].replace(" mm", ""))
        Sensor_WS90_rainRate=   location + ",Measurement=WS90" +  " RainRate(mm/h)="        +str(data['piezoRain'][1]['val'].replace(" mm/Hr", ""))
        Sensor_WS90_rainDay=    location + ",Measurement=WS90" +  " RainDay(mm)="           +str(data['piezoRain'][2]['val'].replace(" mm", ""))
        Sensor_WS90_rainWeek=   location + ",Measurement=WS90" +  " RainWeek(mm)="          +str(data['piezoRain'][3]['val'].replace(" mm", ""))
        Sensor_WS90_rainMonth=  location + ",Measurement=WS90" +  " RainMonth(mm)="         +str(data['piezoRain'][4]['val'].replace(" mm", ""))
        Sensor_WS90_rainYear=   location + ",Measurement=WS90" +  " RainYear(mm)="          +str(data['piezoRain'][5]['val'].replace(" mm", ""))

        #try uploading data to influxDb. Spits out an shows error in logs if.
        try:
            write_api.write(bucket, org, Sensor_WS90_Temp)
            write_api.write(bucket, org, Sensor_WS90_Humid)
            write_api.write(bucket, org, Sensor_WS90_FeelLike)
            write_api.write(bucket, org, Sensor_WS90_DewPoint)
            write_api.write(bucket, org, Sensor_WS90_WindChill)
            write_api.write(bucket, org, Sensor_WS90_WindSpeed)
            write_api.write(bucket, org, Sensor_WS90_GustSpeed)
            write_api.write(bucket, org, Sensor_WS90_DayWindMax)
            write_api.write(bucket, org, Sensor_WS90_Solar)
            write_api.write(bucket, org, Sensor_WS90_UVIndex)
            write_api.write(bucket, org, Sensor_WS90_WindDir)
            write_api.write(bucket, org, Sensor_WS90_rainEvent)
            write_api.write(bucket, org, Sensor_WS90_rainRate)
            write_api.write(bucket, org, Sensor_WS90_rainDay)    
            write_api.write(bucket, org, Sensor_WS90_rainWeek)
            write_api.write(bucket, org, Sensor_WS90_rainMonth)
            write_api.write(bucket, org, Sensor_WS90_rainYear)
            
            print("WS90 posted to influxDB succsessfully")
            
        except: # error for uploading to influxDB"
            print("WARNING!...Error posting WS90 data  to influxDB")
        
    except: #error if cannot get data for WS90
        print("WARNING!...WS90 not avalaible")

    

# WH40 Self-emptying Rain Gauge
####################################################################################################
def WH40():
    try:
        Sensor_WH40_rainEvent=  location + ",Measurement=WH40(rainfall) " +  " RainEvent(mm)="      +str(data['rain'][0]['val'].replace(" mm", ""))
        Sensor_WH40_rainRate=   location + ",Measurement=WH40(rainfall) " +  " RainRate(mm/h)="     +str(data['rain'][1]['val'].replace(" mm/Hr", ""))
        Sensor_WH40_rainDay=    location + ",Measurement=WH40(rainfall) " +  " RainDay(mm)="        +str(data['rain'][2]['val'].replace(" mm", ""))
        Sensor_WH40_rainWeek=   location + ",Measurement=WH40(rainfall) " +  " RainWeek(mm)="       +str(data['rain'][3]['val'].replace(" mm", ""))
        Sensor_WH40_rainMonth=  location + ",Measurement=WH40(rainfall) " +  " RainMonth(mm)="      +str(data['rain'][4]['val'].replace(" mm", ""))
        Sensor_WH40_rainYear=   location + ",Measurement=WH40(rainfall) " +  " RainYear(mm)="       +str(data['rain'][5]['val'].replace(" mm", ""))
        
        write_api.write(bucket, org, Sensor_WH40_rainEvent)
        write_api.write(bucket, org, Sensor_WH40_rainRate)
        write_api.write(bucket, org, Sensor_WH40_rainDay)
        write_api.write(bucket, org, Sensor_WH40_rainWeek)
        write_api.write(bucket, org, Sensor_WH40_rainMonth)
        write_api.write(bucket, org, Sensor_WH40_rainYear)

        print("WH40 posted to influxDB succsessfully")
    except:
        print("WH40-self emptying rain gauge not avalaible")
    
# WH31 multichannel temperature and humidity
####################################################################################################
def WH31():
    
    for i,a in enumerate(data['ch_aisle']):
        try:
            Sensor_WH31Temp=    location + ",Measurement=WH31_channel_" + data['ch_aisle'][i]['channel'] + " " +  " Temperature(C)="   + str(data['ch_aisle'][i]['temp'])
            Sensor_WH31Humid=   location + ",Measurement=WH31_channel_" + data['ch_aisle'][i]['channel'] + " " +  " Humidity(%)="   + str(data['ch_aisle'][i]['humidity'].replace("%", ""))

            write_api.write(bucket, org, Sensor_WH31Temp)
            write_api.write(bucket, org, Sensor_WH31Humid)
            
         
        except:
            print("WARNING!....No data from multi channel temperatures Sensor_ors detected")
            
    print("WH31(s) posted to influxDB succsessfully")   
# WH51 multichannel soil moisuture
####################################################################################################
def WH51():
    
    for i,a in enumerate(data['ch_soil']):
        try:
            Sensor_WH51_SoilMoisture=      location + ",Measurement=WH51_channel_" + data['ch_soil'][i]['channel'] + " " +  " Moisture(%)="   + str(data['ch_soil'][i]['humidity'].replace("%", ""))
            write_api.write(bucket, org, Sensor_WH51_SoilMoisture)
            

        except:
            print("WARNING: No data from soil moisure Sensor (WH51) detected")
            
    print("WH31(s) posted to influxDB succsessfully") 

####################################################################################################
# main program
####################################################################################################
client = InfluxDBClient(url=influxDB_url, token=token)
while True:
    write_api = client.write_api(write_options=SYNCHRONOUS)
    print(str(datetime.now()))
    data = requests.get('http://'+ GW2000_ip_address + '/get_livedata_info?').json()
    WS90()
    GW2000()
    WH40()
    WH31()
    WH51()
    
    print("")
    time.sleep(sample_time - time.monotonic() % sample_time)




        
