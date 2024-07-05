# boot.py -- run on boot-up
import machine  # type: ignore
from secret import *

led_pin = machine.Pin(18, machine.Pin.OUT)

def set_time():
    import ntptime # type: ignore
    import time

    retry_count = 0

    while retry_count < 20:
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
        for i in range(15):
            print(f'connecting to network: try {i + 1}...')
            client.active(True)
            client.connect(wifi_ssid, wifi_password)
            for j in range(2):  
                led_pin.value(0)
                time.sleep(0.25)
                led_pin.value(1)
                time.sleep(0.25)
            if client.isconnected():
                break

        print('network config:', client.ifconfig())

def update_time(client):
    if not client.isconnected():
        clientNew = do_connect(client)

        if clientNew.isconnected():
            set_time()
    else:
        set_time()