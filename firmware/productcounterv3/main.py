import machine # type: ignore
import time
from provisioning import start_provisioning
import ubinascii  # type: ignore
from boot import do_connect, set_time, update_time
from mqtt import connect_mqtt, send_payload, send_health_check, check_process_messages
import network # type: ignore
from secret import firmware_url
from ota import OTAUpdater
import utime # type: ignore
import json
import os

print(ubinascii.hexlify(machine.unique_id()).decode())

led_pin = machine.Pin(13, machine.Pin.OUT)
led2_pin = machine.Pin(12, machine.Pin.OUT)
relay_1 = machine.Pin(33, machine.Pin.OUT)
relay_2 = machine.Pin(32, machine.Pin.OUT)
digital_input = machine.Pin(17, machine.Pin.IN)

relay_1.value(0)
relay_2.value(0)
led_pin.value(1)
led2_pin.value(1)

relay_1_input = machine.Pin(34, machine.Pin.IN)
relay_2_input = machine.Pin(35, machine.Pin.IN)

provision_count = 0
must_provision_count = 0

while provision_count < 12:
    if((relay_1_input.value() == 1) and (relay_2_input.value() == 1)):
        print('provision +1')
        must_provision_count += 1
    
    if must_provision_count > 5:
        relay_1.value(1)
        relay_2.value(1)
        led_pin.value(0)
        led2_pin.value(0)
        start_provisioning()

    time.sleep(0.5)
    provision_count += 1

wifi_client = network.WLAN(network.STA_IF)
do_connect(wifi_client)

##Check for firmware update
if wifi_client.isconnected():
    set_time()
    ota_updater = OTAUpdater(wifi_client, firmware_url, ['main.py', 'boot.py', 'mqtt.py', 'provision.py'])
    ota_updater.download_and_install_update_if_available()

##MQTT
mqtt_client = connect_mqtt()

firmware_version = 0

if 'version.json' in os.listdir():    
    with open('version.json') as f:
        firmware_version = int(json.load(f)['version'])

mqtt_client = send_health_check(wifi_client, mqtt_client, firmware_version, is_boot=True)

message_interval = 5

times = []
timestamps = []

lastTimeUpdate = 946684800 + utime.time()
lastHealthcheck = 946684800 + utime.time()
lastMqttEvent = 946684800 + utime.time()
lastTicks = 0
currentTicks = 0

lastDigitalReading = -1

last_relay_1_val = 0
last_relay_2_val = 0
relay_1_state = False
relay_2_state = False

while True:
    try:
        timestamp = 946684800 + utime.time()

        ## Read digital pin
        currentDigitalReading = digital_input.value()

        if timestamp - lastTimeUpdate > 86400:
            # If it's been a day since last time update
            wifi_client = update_time(wifi_client)
            lastTimeUpdate = timestamp

        if timestamp - lastMqttEvent > 300:
            # send health check every 10 min where no messages were sent
            mqtt_client = send_health_check(wifi_client, mqtt_client,firmware_version)
            lastMqttEvent = timestamp
            lastHealthcheck = timestamp

        if(relay_1_input.value() == 1):
            if(last_relay_1_val == 0):
                 relay_1_state = not relay_1_state 
                 if relay_1_state:
                     relay_1.value(1)
                 else:
                     relay_1.value(0)
            last_relay_1_val = 1
        else:
            last_relay_1_val = 0

        if(relay_2_input.value() == 1):
            if(last_relay_2_val == 0):
                 relay_2_state = not relay_2_state 
                 if relay_2_state:
                     relay_2.value(1)
                 else:
                     relay_2.value(0)
            last_relay_2_val = 1
        else:
            last_relay_2_val = 0


        if (currentDigitalReading == 0 and lastDigitalReading == 1):
            led_pin.value(0)
            currentTicks = utime.ticks_ms()
            if lastTicks > 0:
                ticksDifference = time.ticks_diff(currentTicks, lastTicks)

                if ticksDifference > 500:
                    times.append(ticksDifference)
                    timestamps.append(timestamp)

                    ## Send the data here
                    print(times)
                    print(timestamps)

                    mqtt_client, times, timestamps = send_payload(wifi_client, mqtt_client, times, timestamps)

                    lastMqttEvent = timestamp

            lastTicks = currentTicks
        
        if (currentDigitalReading == 1 and lastDigitalReading == 0):
            led_pin.value(1)

        lastDigitalReading = currentDigitalReading

        ##Check if there are messages
        check_process_messages(mqtt_client)
    except Exception as e:
        print("Exception in main loop", e)
        print(e)