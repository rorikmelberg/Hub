import os
import functools
from webapp.db import get_db
import webapp.DAL.BrewDAL as BrewDAL
import webapp.DAL.SensorDataDAL as SensorDataDAL
import webapp.BO.CookBO as CookBO

from datetime import datetime

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
    currentBrew = BrewDAL.getBrew(brewId)
    
    if currentBrew.BrewId > 0:
        allData = {}

        endTime = datetime.now()

        if currentBrew.EndDate:
            endTime = currentBrew.EndDate
        
        allData['duration'] = currentBrew.Duration
        allData['startDate'] = currentBrew.StartDate.strftime(dateFormatString)
        allData['currentDT'] = datetime.now()
        
        currentDate = endTime
        allData['lastUpdate'] = currentDate.strftime(dateFormatString)

        if date:
            queryStartDate = date
        else:
            queryStartDate = currentBrew.StartDate

        allData['Temp'] = GetTrendData(currentBrew.TempSensorId, queryStartDate, currentDate, False)
        allData['tempTarget'] =  GetTrendData(currentBrew.TempTargetSensorId, queryStartDate, currentDate, True)
    
        allData['Gravity'] = GetTrendData(currentBrew.GravitySensorId, queryStartDate, currentDate, False)
        allData['gravityTarget'] = GetTrendData(currentBrew.GravTargetSensorId, queryStartDate, currentDate, True)

        if len(allData['Temp']) > 0:
            allData['TempCurrent'] = '{0:.2f}'.format(allData['Temp'][-1]['y'])
            lastDataUpdate = datetime.strptime(allData['Temp'][-1]['x'], dateFormatString)
            allData['LastDataUpdate'] = lastDataUpdate.strftime(dateFormatString)
            allData['LastDataStatus'] = (currentDate - lastDataUpdate).total_seconds() < 120
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

def GetTrendData(sensorId, startDate, endDate, isTarget):
    data = SensorDataDAL.getValues(sensorId, startDate, endDate)
    
    print(len(data))
    outputData = []
    for x in data:
        # formattedDate = x.EventDate.strftime(dateFormatString)
        value = {}
        value['x'] = x.EventDate
        value['y'] = x.ValueFloat
        outputData.append(value)

    # to get targets to show, you have to add the end date
    if isTarget:
        value = {}
        value['x'] = endDate
        value['y'] = outputData[-1]['y']
        outputData.append(value)
        
    return outputData
