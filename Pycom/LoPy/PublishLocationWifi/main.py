from network import WLAN
import urequests as requests
import machine
import time

# Your WiFi network credentials
WIFI_SSID = 'your-wifi-ssid'
WIFI_KEY = 'your-wifi-key'

# Get this from the Wia dashboard
DEVICE_SECRET_KEY = 'your-device-secret-key'

# Delay between each event
DELAY = 2

wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()

# Connect to the WiFi network
for net in nets:
    if net.ssid == WIFI_SSID:
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, WIFI_KEY), timeout=5000)
        # while not wlan.isconnected():
        #     machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

print("Connected to Wifi\n")

# Post a Location to the Wia cloud
def post_location(latitude, longitude):
    try:
        url = "https://api.wia.io/v1/locations"
        headers = {"Authorization": "Bearer " + DEVICE_SECRET_KEY, "Content-Type": "application/json"}
        json_data = {"latitude": latitude, "longitude": longitude}
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
    latitude = 35.652832
    longitude = 139.839478
    post_location(latitude, longitude)
    time.sleep(DELAY)
