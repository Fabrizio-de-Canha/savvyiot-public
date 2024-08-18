# boot.py -- run on boot-up
import machine  # type: ignore
from secret import *

led_pin = machine.Pin(13, machine.Pin.OUT)

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
        for i in range(8):
            print(f'connecting to network: try {i + 1}...')
            client.active(True)
            try:
                client.connect(wifi_ssid, wifi_password)
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

        print('network config:', client.ifconfig())

def update_time(client):
    if not client.isconnected():
        clientNew = do_connect(client)

        if clientNew.isconnected():
            set_time()
    else:
        set_time()