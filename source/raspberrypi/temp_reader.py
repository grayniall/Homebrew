import os
import glob
import time
import json
import urllib2
import fnmatch

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
        'id': device_info[0],
        'tempCelsius': device_info[1],
        'tempFarenheit': device_info[2]
        }

        req = urllib2.Request('https://wn394dz7dc.execute-api.eu-west-1.amazonaws.com/v1/temp')
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(data))
        print(response)

while True:
        for root, dirnames,filenames in os.walk(base_dir):
                for dir in fnmatch.filter(dirnames, '28*'):
                        PostTempReadings(read_temp(dir))

        time.sleep(1)