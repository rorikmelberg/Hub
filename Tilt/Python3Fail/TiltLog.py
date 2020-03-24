# Log Tilt data to Hub
import TiltHydrometer
import _thread as thread
import time
import requests
import json
import settings

tiltHydrometer = TiltHydrometer.TiltHydrometerManager(False, 60, 40)
tiltHydrometer.loadSettings()
tiltHydrometer.start()
time.sleep(10)

valuesToSend = []

tiltHydrometer.getValue(colour)

tiltHydrometer.stop()


valuesToSendText = json.dumps(valuesToSend)
print(valuesToSendText)

url = settings.get_url()
res = requests.post('http://' + url + '/tilt/setdata', json=valuesToSendText)
if res.ok:
	print(res.json())

