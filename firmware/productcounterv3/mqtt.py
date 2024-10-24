from umqtt.simple import MQTTClient  # type: ignore
import machine  # type: ignore
import ubinascii  # type: ignore
import time
from boot import do_connect, set_time
import utime # type: ignore
from secret import *
import os
import json

led_pin = machine.Pin(13, machine.Pin.OUT)

macAddress = ubinascii.hexlify(machine.unique_id()).decode()

## OUT
mqtt_data_topic = f'{mqtt_ClientID}/productcounter/{macAddress}/data'
mqtt_health_topic = f'{mqtt_ClientID}/productcounter/{macAddress}/status'
mqtt_startup_topic = f'{mqtt_ClientID}/productcounter/{macAddress}/startup'

## IN
mqtt_control_topic = f'{mqtt_ClientID}/productcounter/{macAddress}/control'

def connect_mqtt():
    client = MQTTClient(f'{mqtt_ClientID}_{macAddress}', mqtt_server, 1883, mqtt_username, mqtt_password)

    ## Retry connections here
    ## Retry 10 times max
    for i in range(5):
        print(f'connecting to mqtt: try {i + 1}...')
        try:
            client.set_callback(recieve_mqtt)
            client.connect()
            for j in range(5):  
                led_pin.value(0)
                time.sleep(0.1)
                led_pin.value(1)
                time.sleep(0.1)
            print('connected to mqtt server')
            client.subscribe(mqtt_control_topic)
            return client
        except OSError:
            for j in range(5):  
                led_pin.value(0)
                time.sleep(0.1)
                led_pin.value(1)
                time.sleep(0.1)

    print('failed to connect to mqtt server')

    return client

def send_health_check(wifi_client, mqtt_client, firmware_version, is_boot=False):
    ## Get firmware version

    if is_boot:
        topic = mqtt_startup_topic
    else:
        topic = mqtt_health_topic

    if not wifi_client.isconnected():
        do_connect(wifi_client)
        if wifi_client.isconnected():
            set_time()

    if wifi_client.isconnected():
        rssi = wifi_client.status('rssi')
        timestamp = 946684800 + utime.time()

        ## If the timestamp is less than 2001
        if timestamp < 978307200:
            set_time()
            timestamp = 946684800 + utime.time()
            
        try:
            mqtt_client.publish(topic, f'{{"timestamp":{timestamp},"rssi":{rssi},"firmware_version":{firmware_version}}}')
        except OSError:
                mqtt_client = connect_mqtt()
                try:
                    mqtt_client.publish(topic, f'{{"timestamp":{timestamp},"rssi":{rssi},"firmware_version":{firmware_version}}}')
                except OSError:
                    return
    
    return mqtt_client

def send_payload(wifi_client, mqtt_client, times, timestamps):
    
    if not wifi_client.isconnected():
        do_connect(wifi_client)
        if wifi_client.isconnected():
            set_time()
            if timestamps[0] - 946684800 < 7200:
                count = 0
                for i in timestamps:
                    timestamps[count] = 946684800 + utime.time() - i + 946684800

    if wifi_client.isconnected():
        rssi = wifi_client.status('rssi')
        timestamp = 946684800 + utime.time()

        ## If the timestamp is less than 2001
        if timestamp < 978307200:
            set_time()
            timestamp = 946684800 + utime.time()

        if len(times) > 0:
            count = 0
            body = ''
            for i in times:
                if count == 0:
                    body = f'{{"type": "cycle_time_1","value":{i},"timestamp":{timestamps[count]}}}'
                else:
                    body = f'{body},{{"type": "cycle_time_1","value":{i},"timestamp":{timestamps[count]}}}'
                count += 1

            try:
                mqtt_client.publish(mqtt_data_topic, f'{{"data":[{body}],"timestamp":{timestamp},"rssi":{rssi}}}')
            except OSError:
                mqtt_client = connect_mqtt()
                try:
                    mqtt_client.publish(mqtt_data_topic, f'{{"data":[{body}],"timestamp":{timestamp},"rssi":{rssi}}}')
                except OSError:
                    ## If failed to send message just return for now
                    return times, timestamps
            return mqtt_client, [], []
    else:
        return mqtt_client,times, timestamps

def check_process_messages(mqtt_client):
    try:
        mqtt_client.check_msg()
    except OSError as e:
        print('failed to check message')



def recieve_mqtt(topic, msg):
    if(topic.decode().split("/")[-1] == "control"):
        try:
            jsonObj = json.loads(msg)
            if(jsonObj['type'] == "reset"):
                machine.reset()
        except:
            print("error reading message")
