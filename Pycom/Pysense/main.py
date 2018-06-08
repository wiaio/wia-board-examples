from network import WLAN
from pysense import Pysense
from SI7006A20 import SI7006A20
import urequests as requests
import socket
import time

py = Pysense()
si = SI7006A20(py)

# Your WiFi network credentials
WIFI_SSID = 'your-wifi-ssid'
WIFI_KEY = 'your-wifi-password'

# Get this from the Wia dashboard
DEVICE_SECRET_KEY = 'your-wifi-ssid'

url = "https://api.wia.io/v1/events"
headers = { "Authorization": "Bearer " + DEVICE_SECRET_KEY, "Content-Type": "application/json" }

wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()

# Connect to the WiFi network
for net in nets:
    if net.ssid == WIFI_SSID:
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, WIFI_KEY), timeout=5000)
        print('Connecting...')
        while not wlan.isconnected():
             machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break


# Post an Event to the Wia cloud
def post_event(name, data):
    try:
        json_data = { "name": name, "data": data }
        print str(json_data)
        if json_data is not None:
            req = requests.post(url=url, headers=headers, json=json_data)
            return req.json()
        else:
            pass
    except:
        pass

# main loop
while True:
    # Takes the temperature from the Pysense expansion board
    post_event("temperature", si.temperature())
    time.sleep(10)
