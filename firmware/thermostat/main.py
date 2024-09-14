import machine  # type: ignore
import time
import utime # type: ignore
from boot import do_connect, set_time, update_time
from mqtt import connect_mqtt, send_payload, send_health_check, check_process_messages
import network # type: ignore
from ota import OTAUpdater
from secret import firmware_url
import os
import json
import ubinascii  # type: ignore
from max6675 import MAX6675
from thermostat import OverHeating, savvyThermostat

print(ubinascii.hexlify(machine.unique_id()).decode())

led_pin = machine.Pin(13, machine.Pin.OUT)
status_led_pin = machine.Pin(12, machine.Pin.OUT)
relay_1 = machine.Pin(33, machine.Pin.OUT)
relay_2 = machine.Pin(32, machine.Pin.OUT)
digital_input = machine.Pin(17, machine.Pin.IN)

relay_1_input = machine.Pin(34, machine.Pin.IN)
relay_2_input = machine.Pin(35, machine.Pin.IN)

## Temp pins
so = machine.Pin(19, machine.Pin.IN)
sck = machine.Pin(18, machine.Pin.OUT)
cs = machine.Pin(5, machine.Pin.OUT)

## WIFI
# wifi_client = network.WLAN(network.STA_IF)
# do_connect(wifi_client)

##Check for firmware update
# if wifi_client.isconnected():
#     set_time()
#     ota_updater = OTAUpdater(wifi_client, firmware_url, ['main.py', 'boot.py', 'mqtt.py'])
#     ota_updater.download_and_install_update_if_available()


##MQTT
# mqtt_client = connect_mqtt()

# firmware_version = 0

# if 'version.json' in os.listdir():    
#     with open('version.json') as f:
#         firmware_version = int(json.load(f)['version'])

# mqtt_client = send_health_check(wifi_client, mqtt_client, firmware_version)

message_interval = 5

times = []
timestamps = []

lastTimeUpdate = 946684800 + utime.time()
lastHealthcheck = 946684800 + utime.time()
lastTicks = 0
currentTicks = 0

lastDigitalReading = -1

maxTempSensor = MAX6675()
thermostat = savvyThermostat()
ticksOverheatingLED = 0
lastTempReadingTicks = utime.ticks_ms()

status_led_pin.value(1)
isOverheating = False

while True:
    timestamp = 946684800 + utime.time()

    ## Read digital pin
    currentDigitalReading = digital_input.value()

    ## Read temperature

    if(utime.ticks_ms() - lastTempReadingTicks > 1000):
        print(maxTempSensor.readCelsius())
        isOverheating = False
        try:
            temp = maxTempSensor.readCelsius()
            try:
                relay_1.value(thermostat.determainRelayState(temperature=temp))
            except OverHeating:  
                isOverheating = True 
                relay_1.value(0)
        except :
            print('Failed to read temperature')

        lastTempReadingTicks = utime.ticks_ms()

    if(isOverheating and (utime.ticks_ms()-ticksOverheatingLED > 200)):
        status_led_pin.value(0)
            
    if(isOverheating and (utime.ticks_ms()-ticksOverheatingLED > 400)):
        status_led_pin.value(1)
        ticksOverheatingLED = utime.ticks_ms()
    
    if not isOverheating:
        status_led_pin.value(1)

    # if timestamp - lastTimeUpdate > 86400:
    #     # If it's been a day since last time update
    #     update_time(wifi_client)
    #     lastTimeUpdate = timestamp

    # if timestamp - lastHealthcheck > 1800:
    #     # send health check every hour
    #     mqtt_client = send_health_check(wifi_client, mqtt_client,firmware_version)
    #     lastHealthcheck = timestamp

    ##Check if there are messages
    # check_process_messages(mqtt_client)
