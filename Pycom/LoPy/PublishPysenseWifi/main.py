from network import WLAN
import urequests as requests
import machine
import time
from LTR329ALS01 import LTR329ALS01
from SI7006A20 import SI7006A20
from MPL3115A2 import MPL3115A2

# Light Sensor
l = LTR329ALS01()
# Temperature and Humidity Sensor
t = SI7006A20()
# Pressure Sensor
p = MPL3115A2()

# Your WiFi network credentials
WIFI_SSID = 'your-wifi-ssid'
WIFI_KEY = 'your-wifi-key'

# Get this from the Wia dashboard (it should begin with d_sk)
DEVICE_SECRET_KEY = 'your-device-secret-key'

# Delay between each event
DELAY = 3

wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()

# Connect to the WiFi network
for net in nets:
    if net.ssid == WIFI_SSID:
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, WIFI_KEY), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

print("Connected to Wifi\n")

# Post an Event to the Wia cloud
def post_event(name, data):
    try:
        url = "https://api.wia.io/v1/events"
        headers = {"Authorization": "Bearer " + DEVICE_SECRET_KEY, "Content-Type": "application/json"}
        json_data = {"name": name, "data": data}
        if json_data is not None:
            print(json_data)
            req = requests.post(url=url, headers=headers, json=json_data)
            print(req.json())
            return req.json()
        else:
            pass
    except:
        pass

# Run this loop continuously
while True:
    light = l.light()
    temperature = t.temperature()

    post_event("light", light[0])
    # post_event("humidity", t.humidity())
    post_event("temperature", temperature)
    # post_event("pressure", p.pressure())
    time.sleep(DELAY)
