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
            return req.json()
        else:
            pass
    except:
        pass

# Run this loop continuously
while True:
    temperature = 21.5
    post_event("temperature", temperature)
    time.sleep(DELAY)
