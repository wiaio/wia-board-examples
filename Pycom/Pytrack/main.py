from network import WLAN
from pytrack import Pytrack
import urequests as requests
from L76GNSS import L76GNSS
import socket
import time
import pycom

py = Pytrack()
gps = L76GNSS(py, timeout=30)

# Your WiFi network credentials
WIFI_SSID = 'Dogpatch-legacy'
WIFI_KEY = '*warofthebuttons94'

# Get this from the Wia dashboard
DEVICE_SECRET_KEY = 'd_sk_T8NGE0j0up14eftVwQvPIxNm'

# Delay between each event
DELAY = 30

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
def post_location(latitude, longitude):
    try:
        url = "https://api.wia.io/v1/locations"
        headers = {"Authorization": "Bearer " + DEVICE_SECRET_KEY, "Content-Type": "application/json"}
        json_data = {"latitude": str(latitude), "longitude": str(longitude)}
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

lat = 53
lng = -6

# main loop
while True:
    # Get coordinates from pytrack
    coord = gps.coordinates()
    if not coord == (None, None):
        lat, lng = coord
    post_location(lat, lng)
    time.sleep(2)
