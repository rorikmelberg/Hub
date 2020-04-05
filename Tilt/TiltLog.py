#Simple utility to test if the Tilt Hydrometer has been connected properly to the raspberry pi.
import TiltHydrometer
import thread
import time
import requests
import json
import settings
import logging

logging.basicConfig(filename='TiltLog.log', level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

while True:

	logging.info('TiltLog Start')
	logging.info('URL: %s', settings.get_url())
	logging.info('Loop Timeout: %s', settings.get_looptimeout())
	logging.info('Debug: %s', settings.get_debug())

	try:
		tiltHydrometer = TiltHydrometer.TiltHydrometerManager(True, 60, 40)
		tiltHydrometer.loadSettings()
		tiltHydrometer.start()

		debug = settings.get_debug()

		while True:
			time.sleep(settings.get_looptimeout())
			
			valuesToSend = []

			value = tiltHydrometer.getValue('Black')

			logging.debug('Temperature: %s', value.temperature)
			logging.debug('Gravity: %s', value.gravity)

			valuesToSend = [value.temperature, value.gravity]

			valuesToSendText = json.dumps(valuesToSend)

			url = settings.get_url()
			res = requests.post('http://' + url + '/tilt/setdata', json=valuesToSendText)
			
			logging.debug(res.json())
			
	except Exception as inst:
		logging.error(type(inst))
		logging.error(inst.args)
		logging.error(inst.args)
		
		tiltHydrometer.stop()
	
	logging.info('TiltLog End')
	