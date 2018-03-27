from network import WLAN
import urequests as requests
import machine
import time
import pycom

# Your WiFi network credentials
WIFI_SSID = ''
WIFI_KEY = ''

# Get this from the Wia dashboard
DEVICE_SECRET_KEY = ''

# Delay between each event
DELAY = 5

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
        url = "https://api.wia.io/v1/events"
        headers = {"Authorization": "Bearer " + DEVICE_SECRET_KEY, "Content-Type": "application/json"}
        json_data = {"name": name, "data": data}
        if json_data is not None:
            req = requests.post(url=url, headers=headers, json=json_data)
            if req.status_code is not 200:
                machine.reset()
            else:
                print(json_data)
            return req.json()
        else:
            pass
    except:
        pass

# Run this loop continuously
while True:
    temperature = 21.5
    post_event("temperature", temperature)
    if not wlan.isconnected():
         print("Not connected to WiFi")
    time.sleep(DELAY)
    machine.idle()

