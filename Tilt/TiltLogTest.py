#Simple utility to test if the Tilt Hydrometer has been connected properly to the raspberry pi.
import TiltHydrometer
import thread
import time
import requests
import json
import settings
import logging

valuesToSend = []
valuesToSend = [100.0, 1.098]
valuesToSendText = json.dumps(valuesToSend)
url = settings.get_url()
res = requests.post('http://' + url + '/tilt/setdata', json=valuesToSendText)
