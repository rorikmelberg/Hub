#Simple utility to test if the Tilt Hydrometer has been connected properly to the raspberry pi.
import time
import requests
import json
import settings
import logging
import random

logging.basicConfig(filename='PT100Log.log', level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def SendSensorData(sensorId, value):
	valuesToSend = {}
	valuesToSend['SensorId'] = sensorId
	valuesToSend['Value'] = value
	logging.debug('Sensor: {0} Value: {1}'.format(sensorId, value))
	
	print (valuesToSend)
	url = settings.get_url()
	res = requests.post('http://' + url + '/sensors/setdata', json=valuesToSend)
	print(res)
	print(res.content)
if __name__ == "__main__":
	while True:

		logging.info('PT100Log Start')
		logging.info('URL: %s', settings.get_url())
		logging.info('Loop Timeout: %s', settings.get_looptimeout())
		logging.info('Debug: %s', settings.get_debug())

		try:
			
			debug = settings.get_debug()

			while True:
				temp = random.randint(50,100)
				gravity = (random.randint(1010, 1080)/1000)
			
				SendSensorData(2, temp)
				SendSensorData(4, gravity)
				time.sleep(settings.get_looptimeout())

		except Exception as inst:
			logging.error(type(inst))
			logging.error(inst.args)
			logging.error(inst.args)
			
		logging.info('PT100Log End')

			