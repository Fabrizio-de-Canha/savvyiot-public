import machine  # type: ignore
import time
import utime # type: ignore
from boot import do_connect, set_time, update_time
from mqtt import connect_mqtt, send_payload, send_health_check
import network # type: ignore
from ota import OTAUpdater
from secret import firmware_url
import os
import json

led_pin = machine.Pin(18, machine.Pin.OUT)
relay_1 = machine.Pin(32, machine.Pin.OUT)
relay_2 = machine.Pin(33, machine.Pin.OUT)
digital_input = machine.Pin(16, machine.Pin.IN)

## WIFI
wifi_client = network.WLAN(network.STA_IF)
do_connect(wifi_client)

##MQTT
mqtt_client = connect_mqtt()

##Check for firmware update
if wifi_client.isconnected():
    set_time()
    ota_updater = OTAUpdater(wifi_client, firmware_url, ['main.py', 'boot.py', 'mqtt.py'])
    ota_updater.download_and_install_update_if_available()
    
firmware_version = 0

if 'version.json' in os.listdir():    
    with open('version.json') as f:
        firmware_version = int(json.load(f)['version'])

mqtt_client = send_health_check(wifi_client, mqtt_client, firmware_version)

message_interval = 5

times = []
timestamps = []

lastTimeUpdate = 946684800 + utime.time()
lastHealthcheck = 946684800 + utime.time()
lastTicks = 0
currentTicks = 0

lastDigitalReading = -1

while True:
    timestamp = 946684800 + utime.time()

    ## Read digital pin
    currentDigitalReading = digital_input.value()

    if timestamp - lastTimeUpdate > 86400:
        # If it's been a day since last time update
        update_time(wifi_client)
        lastTimeUpdate = timestamp

    if timestamp - lastHealthcheck > 3600:
        # send health check every hour
        mqtt_client = send_health_check(wifi_client, mqtt_client,firmware_version)
        lastHealthcheck = timestamp


    if (currentDigitalReading == 0 and lastDigitalReading == 1):
        led_pin.value(0)
        currentTicks = utime.ticks_ms()
        if lastTicks > 0:
            ticksDifference = time.ticks_diff(currentTicks, lastTicks)

            if ticksDifference > 10:
                times.append(ticksDifference)
                timestamps.append(timestamp)

                ## Send the data here
                print(times)
                print(timestamps)

                mqtt_client, times, timestamps = send_payload(wifi_client, mqtt_client, times, timestamps)
        
        lastTicks = currentTicks
    
    if (currentDigitalReading == 1 and lastDigitalReading == 0):
        led_pin.value(1)

    lastDigitalReading = currentDigitalReading

