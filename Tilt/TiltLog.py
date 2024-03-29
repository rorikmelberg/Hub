#Simple utility to test if the Tilt Hydrometer has been connected properly to the raspberry pi.
import TiltHydrometer
import thread
import time
import requests
import json
import settings
import logging

logging.basicConfig(filename='TiltLog.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

GRAVITYSENSORBLACK = 4
TEMPSENSORBLACK = 6

def SendSensorData(sensorId, value):
	valuesToSend = {}
	valuesToSend['SensorId'] = sensorId
	valuesToSend['Value'] = value
	
	logging.info('Sensor: {0} Value: {1}'.format(sensorId, value))
	
	url = settings.get_url()
	res = requests.post(url + '/sensors/setdata', json=valuesToSend)

logging.info('TiltLog Start')
logging.info('URL: %s', settings.get_url())
logging.info('Loop Timeout: %s', settings.get_looptimeout())
logging.info('Debug: %s', settings.get_debug())

tiltHydrometer = TiltHydrometer.TiltHydrometerManager(True, 60, 40)
tiltHydrometer.loadSettings()
tiltHydrometer.start()

while True:
	try:
		
		debug = settings.get_debug()

		valuesToSend = []

		value = tiltHydrometer.getValue('Black')
		
		logging.debug('Temperature: %s', value.temperature)
		logging.debug('Gravity: %s', value.gravity)

		SendSensorData(GRAVITYSENSORBLACK, value.gravity)
		SendSensorData(TEMPSENSORBLACK, value.temperature)

	except Exception as inst:
		logging.error(type(inst))
		logging.error(inst.args)
		logging.error(inst.args)

	# Sleep
	time.sleep(settings.get_looptimeout())

logging.info('Exiting')