from umqtt.simple import MQTTClient  # type: ignore
import machine  # type: ignore
import ubinascii  # type: ignore
import time
from boot import do_connect
import utime # type: ignore

led_pin = machine.Pin(18, machine.Pin.OUT)

mqtt_username = 'test:test'
mqtt_password = '!Q2w3e4r5t'
mqtt_server = '102.22.83.11'
mqtt_ClientID = 'test'

macAddress = ubinascii.hexlify(machine.unique_id()).decode()

mqtt_data_topic = f'{mqtt_ClientID}/productcounter/{macAddress}/data'

def recieve_mqtt(topic, msg):
    print('received message %s on topic %s' % (msg, topic))

def connect_mqtt():
    client = MQTTClient(f'{mqtt_ClientID}_{macAddress}', mqtt_server, 1883, mqtt_username, mqtt_password)

    ## Retry connections here
    ## Retry 10 times max
    for i in range(10):
        print(f'connecting to mqtt: try {i + 1}...')
        try:
            client.connect()
            for j in range(5):  
                led_pin.value(0)
                time.sleep(0.1)
                led_pin.value(1)
                time.sleep(0.1)
            print('connected to mqtt server')
            return client
        except OSError:
            for j in range(5):  
                led_pin.value(0)
                time.sleep(0.1)
                led_pin.value(1)
                time.sleep(0.1)

    print('failed to connect to mqtt server')

    return client

def send_health_check(mqttClient):
    return

## {"data":[{"cycle_time":110558,"cycle_completed_timestamp":1720121276}],"timestamp":1720121276,"rssi":-68}

def send_payload(wifi_client, mqtt_client, times, timestamps):
    if not wifi_client.isconnected():
        do_connect(wifi_client)

    if wifi_client.isconnected():
        rssi = wifi_client.status('rssi')
        timestamp = 946684800 + utime.time()
        if len(times) > 0:
            count = 0
            body = ''
            for i in times:
                if count == 0:
                    body = f'{{"cycle_time":{i},"cycle_completed_timestamp":{timestamps[count]}}}'
                else:
                    body = f'{body},{{"cycle_time":{i},"cycle_completed_timestamp":{timestamps[count]}}}'
                count += 1

            print('publishing')
            mqtt_client.publish(mqtt_data_topic, f'{{"data":[{body}],"timestamp":{timestamp},"rssi":{rssi}}}')
            return [], []
    else:
        return times, timestamps