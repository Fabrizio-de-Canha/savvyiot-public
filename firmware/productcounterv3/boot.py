# boot.py -- run on boot-up
import machine  # type: ignore
from secret import *
import os

led_pin = machine.Pin(13, machine.Pin.OUT)
led2_pin = machine.Pin(12, machine.Pin.OUT)
WIFI_CONFIG_FILE = 'wifi_config.txt'

def load_wifi_credentials():
    """Load WiFi credentials from file."""
    if WIFI_CONFIG_FILE in os.listdir():
        print('wifi creds found')
        with open(WIFI_CONFIG_FILE, 'r') as f:
            ssid = f.readline().strip()
            password = f.readline().strip()
            return ssid, password
    return None, None

def set_time():
    import ntptime # type: ignore
    import time

    retry_count = 0

    while retry_count < 5:
        retry_count += 1
        try:
            print(f'attempt to set time: {retry_count}')
            ntptime.settime()
            break
        except OSError:
            time.sleep(1)

def do_connect(client):
    import time    
    if not client.isconnected():
        ssid, password = load_wifi_credentials()
        if ssid and password:
            for i in range(8):
                print(f'connecting to network {ssid}: try {i + 1}...')
                client.active(True)
                try:
                    client.connect(ssid, password)
                except OSError:
                    print('failed to connect to wifi')
                for j in range(2):  
                    led_pin.value(0)
                    time.sleep(0.25)
                    led_pin.value(1)
                    time.sleep(0.25)
                if client.isconnected():
                    print('connected to wifi')
                    break
        else:
            while True:
                led_pin.value(0)
                led2_pin.value(1)
                time.sleep(0.25)
                led_pin.value(1)
                led2_pin.value(0)
                time.sleep(0.25)

        print('network config:', client.ifconfig())

def update_time(client):
    try:
        if not client.isconnected():
            clientNew = do_connect(client)

            if clientNew.isconnected():
                set_time()
                return clientNew
        else:
            set_time()
            return client
    except Exception as e:
        print('failed to set time')
        print(e)