#Simple utility to test if the Tilt Hydrometer has been connected properly to the raspberry pi.
import TiltHydrometer
import thread
import time
import requests
import json
import settings

tiltHydrometer = TiltHydrometer.TiltHydrometerManager(True, 60, 40)
tiltHydrometer.loadSettings()
tiltHydrometer.start()
time.sleep(10)

valuesToSend = []

value = tiltHydrometer.getValue('Black')

tiltHydrometer.stop()

print 'Temperature'
print value.temperature
print 'Gravity'
print value.gravity

valuesToSend = [value.temperature, value.gravity]

valuesToSendText = json.dumps(valuesToSend)
print(valuesToSendText)

url = settings.get_url()
res = requests.post('http://' + url + '/tilt/setdata', json=valuesToSendText)
if res.ok:
	print(res.json())
