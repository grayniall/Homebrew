import os
import glob
import time
import json
import requests
import fnmatch
import datetime
import config

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'

def read_temp_raw(device_id):
        print(device_id)
        f = open(base_dir + device_id + '/w1_slave' , 'r')
        lines = f.readlines()
        f.close()
        return lines

def read_temp(device_id):
        lines = read_temp_raw(device_id)

        while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                lines = read_temp_raw()

        equals_pos = lines[1].find('t=')

        if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_degree_c = float(temp_string) / 1000.0
                temp_degree_f = temp_degree_c * 9.0 / 5.0 + 32.0
                return device_id,temp_degree_c, temp_degree_f

def PostTempReadings(device_info):
        data = {
                'monitorId': device_info[0],
                'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'tempCelsius': device_info[1],
                'tempFarenheit': device_info[2]
        }

        headers = {
                'Content-Type': 'application/json',
                'x-api-key': temp_config.aws_config['key']
        }

        url = temp_config.aws_config['url']
        r = requests.post(url, headers=headers, data=json.dumps(data))
        print(r)

while True:
        for root, dirnames,filenames in os.walk(base_dir):
                for dir in fnmatch.filter(dirnames, '28*'):
                        PostTempReadings(read_temp(dir))

        time.sleep(60)