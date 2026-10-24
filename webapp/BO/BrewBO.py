import os
import functools
import sys
from pathlib import Path
from datetime import datetime
from datetime import timedelta
from statistics import mean

parent_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(parent_dir))

from db import get_db
import DAL.BrewDAL as BrewDAL
import DAL.SensorDataDAL as SensorDataDAL
import BO.CookBO as CookBO


from flask import current_app
from flask import jsonify

dateFormatString = '%Y-%m-%d %H:%M:%S.%f'

def GenerateTargetData(start, end, value):
    series = []
    
    valPair = {}
    valPair['x'] = start.strftime(dateFormatString)
    valPair['y'] = value
    series.append(valPair)

    valPair = {}
    valPair['x'] = end.strftime(dateFormatString)
    valPair['y'] = value
    series.append(valPair)

    return series

def GetBrewData(brewId, date):
    current_app.logger.debug('BrewBO.GetBrewData {} {}'.format(brewId, date))
    
    try:
        currentBrew = BrewDAL.getBrew(brewId)
        
        if currentBrew.BrewId > 0:
            allData = {}

            endTime = datetime.now().strftime(dateFormatString)
            
            if currentBrew.EndDate:
                endTime = currentBrew.EndDate
            else:
                endTime = datetime.now()

            allData['duration'] = currentBrew.Duration
            allData['startDate'] = currentBrew.StartDate.strftime(dateFormatString)
            allData['currentDT'] = datetime.now().strftime(dateFormatString)
            
            
            allData['lastUpdate'] = datetime.now().strftime(dateFormatString)

            if date:
                queryStartDate = date
            else:
                queryStartDate = currentBrew.StartDate

            allData['Temp'] = GetTrendData(currentBrew.TempSensorId, queryStartDate, endTime, False)
            allData['TiltTemp'] = GetTrendData(currentBrew.TiltTempSensorId, queryStartDate, endTime, False)
            allData['tempTarget'] =  GetTrendData(currentBrew.TempTargetSensorId, currentBrew.StartDate, endTime, True)
        
            allData['Gravity'] = GetTrendData(currentBrew.GravitySensorId, queryStartDate, endTime, False)
            allData['gravityTarget'] = GetTrendData(currentBrew.GravTargetSensorId, currentBrew.StartDate, endTime, True)

            
            if len(allData['Temp']) > 0:
                allData['TempCurrent'] = '{0:.2f}'.format(allData['Temp'][-1]['y'])
                lastDataUpdate = datetime.strptime(allData['Temp'][-1]['x'], dateFormatString)
                allData['LastDataUpdate'] = lastDataUpdate.strftime(dateFormatString)
                allData['LastDataStatus'] = (endTime - lastDataUpdate).total_seconds() < 120
            else:
                allData['LastDataUpdate'] = 'None'
                allData['LastDataStatus'] = False

            if len(allData['Gravity']) > 0:
                allData['GravityCurrent'] = '{0:.3f}'.format(allData['Gravity'][-1]['y'])

            if date:
                queryStartDate = date
            else:
                queryStartDate = currentBrew.StartDate


            return jsonify(allData)

        return jsonify('')

    except Exception as ex:
        current_app.logger.exception(ex)
        current_app.logger.error(ex)
        raise ex

def GetAveragteBrewData(brewId, minutesBack):
    current_app.logger.debug('BrewBO.GetBrewData {} {}'.format(brewId, minutesBack))
    
    try:
        currentBrew = BrewDAL.getBrew(brewId)
        
        if currentBrew.BrewId > 0:
            allData = {}

            endTime = datetime.now().strftime(dateFormatString)

            current_app.logger.debug(currentBrew.EndDate)
            
            if currentBrew.EndDate:
                endTime = currentBrew.EndDate
            else:
                endTime = datetime.now()

            allData['duration'] = currentBrew.Duration
            allData['startDate'] = currentBrew.StartDate.strftime(dateFormatString)
            allData['currentDT'] = datetime.now().strftime(dateFormatString)
            
            
            allData['lastUpdate'] = datetime.now().strftime(dateFormatString)

            if date:
                queryStartDate = date
            else:
                queryStartDate = currentBrew.StartDate

            allData['Temp'] = GetTrendData(currentBrew.TempSensorId, queryStartDate, endTime, False)
            allData['TiltTemp'] = GetTrendData(currentBrew.TiltTempSensorId, queryStartDate, endTime, False)
            allData['tempTarget'] =  GetTrendData(currentBrew.TempTargetSensorId, currentBrew.StartDate, endTime, True)
        
            allData['Gravity'] = GetTrendData(currentBrew.GravitySensorId, queryStartDate, endTime, False)
            allData['gravityTarget'] = GetTrendData(currentBrew.GravTargetSensorId, currentBrew.StartDate, endTime, True)

            
            if len(allData['Temp']) > 0:
                allData['TempCurrent'] = '{0:.2f}'.format(allData['Temp'][-1]['y'])
                lastDataUpdate = datetime.strptime(allData['Temp'][-1]['x'], dateFormatString)
                allData['LastDataUpdate'] = lastDataUpdate.strftime(dateFormatString)
                allData['LastDataStatus'] = (endTime - lastDataUpdate).total_seconds() < 120
            else:
                allData['LastDataUpdate'] = 'None'
                allData['LastDataStatus'] = False

            if len(allData['Gravity']) > 0:
                allData['GravityCurrent'] = '{0:.3f}'.format(allData['Gravity'][-1]['y'])

            if date:
                queryStartDate = date
            else:
                queryStartDate = currentBrew.StartDate


            return jsonify(allData)

        return jsonify('')

    except Exception as ex:
        current_app.logger.exception(ex)
        current_app.logger.error(ex)
        raise ex

def GetTrendData(sensorId, startDate, endDate, isTarget):
    data = SensorDataDAL.getValues(sensorId, startDate, endDate)
    
    outputData = []
    for x in data:
        # formattedDate = x.EventDate.strftime(dateFormatString)
        value = {}
        value['x'] = x.EventDate
        value['y'] = x.ValueFloat
        outputData.append(value)

    # to get targets to show, you have to add the end date
    if len(outputData) >0 and isTarget:
        value = {}
        value['x'] = endDate.strftime(dateFormatString)
        value['y'] = outputData[-1]['y']
        outputData.append(value)
        
    return outputData

def GetBrew15MinAverage():
    startDate = datetime.now() - timedelta(minutes=15)
    endDate = datetime.now()
   
    brewId = BrewDAL.getCurrentBrewId()
    if brewId > 0:
        currentBrew = BrewDAL.getBrew(brewId)

        returnData = {'name': 'Fermenter 1',
                        'temp_unit': 'F',
                        }
        returnData['aux_temp'] = GetAverageTrendData(currentBrew.TempSensorId, startDate, endDate, False)
        returnData['temp'] = GetAverageTrendData(currentBrew.TiltTempSensorId, startDate, endDate, False)
        returnData['gravity'] = GetAverageTrendData(currentBrew.GravitySensorId, startDate, endDate, False)
    else:
        returnData = {}
        
    return returnData
    
def GetAverageTrendData(sensorId, startDate, endDate, isTarget):    
    data = SensorDataDAL.getValues(sensorId, startDate, endDate)
    
    outputData = []    

    lastDate = None
    lastValue = None
    totalSeconds = 0.0
    tempSeconds = 0.0
    for sample in data:
        if lastDate != None:
            diff = (datetime.fromisoformat(sample.EventDate) - lastDate)
            seconds = diff.seconds
            tempSeconds = tempSeconds + (lastValue * seconds)
            totalSeconds = totalSeconds + seconds
        lastDate = datetime.fromisoformat(sample.EventDate) #2026-10-23 12:50:30.036721
        lastValue = sample.ValueFloat
    avg = tempSeconds / totalSeconds

    return avg



