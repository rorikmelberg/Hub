import time
import requests
import json
import settings
import logging
import random
import board

import PT100Funcs


logging.basicConfig(filename='PT100Log.log', level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.getLogger().addHandler(logging.StreamHandler())

def SendSensorData(sensorId, value):
	valuesToSend = {}
	valuesToSend['SensorId'] = sensorId
	valuesToSend['Value'] = value
	
	logging.info('Sensor: {0} Value: {1}'.format(sensorId, value))
	
	url = settings.get_url()
	res = requests.post('http://' + url + '/sensors/setdata', json=valuesToSend)
	
if __name__ == "__main__":
	logging.info('PT100Log Start')
	logging.info('URL: %s', settings.get_url())
	logging.info('Loop Timeout: %s', settings.get_looptimeout())
	logging.info('Debug: %s', settings.get_debug())

	tempSensor = PT100Funcs.setupSensor(board.D5)
	while True:
		try:
			
			debug = settings.get_debug()
			tempVals = PT100Funcs.readTemp(tempSensor)
			SendSensorData(2, round(tempVals['tempF'], 1))
			time.sleep(settings.get_looptimeout())

		except Exception as inst:
			logging.error(type(inst))
			logging.error(inst.args)
			logging.error(inst.args)
			
	logging.info('PT100Log End')

			