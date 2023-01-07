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
    currentSensorData = SensorDataDAL.getLastDataForBrew(brewId)
    print(currentSensorData)

    if currentBrew.BrewId > 0:
        allData = {}

        endTime = datetime.now()

        if currentBrew.EndDate:
            endTime = currentBrew.EndDate
        
        allData['duration'] = currentBrew.Duration
        allData['startDate'] = currentBrew.StartDate.strftime(dateFormatString)
        allData['currentDT'] = datetime.now()
        
        allData['tempTarget'] = GenerateTargetData(currentBrew.StartDate, endTime, currentBrew.TempTarget)
        allData['gravityTarget'] = GenerateTargetData(currentBrew.StartDate, endTime, currentBrew.GravityTarget)
        currentDate = endTime
        allData['lastUpdate'] = currentDate.strftime(dateFormatString)
        
        datas = []
        
        if date:
            datas = SensorDataDAL.getDataForBrew(currentBrew.BrewId, date)
        else:
            datas = SensorDataDAL.getDataForBrew(currentBrew.BrewId)
        
        temps = []
        gravities = []
        
        # get current datas from the first item in the list
        if currentSensorData:
            allData['TempCurrent'] = '{0:.2f}'.format(currentSensorData.Temp)
            allData['GravityCurrent'] = '{0:.3f}'.format(currentSensorData.Gravity)
            allData['LastDataStatus'] = (currentDate - currentSensorData.EventDate).total_seconds() < 120
            allData['LastDataUpdate'] = currentSensorData.EventDate.strftime(dateFormatString)
            
        for x in datas:
            formattedDate = x.EventDate.strftime(dateFormatString)
            temp = {}
            temp['x'] = formattedDate
            temp['y'] = x.Temp
            temps.append(temp)

            gravity = {}
            gravity['x'] = formattedDate
            gravity['y'] = x.Gravity
            gravities.append(gravity)
            
        allData['Temp'] = temps
        allData['Gravity'] = gravities
        
        return jsonify(allData)

    return jsonify('')

# def ProcessSubscriptions(BrewId)
