import os
import functools
from webapp.db import get_db
import webapp.DAL.TiltBrewDAL as TiltBrewDAL
import webapp.DAL.TiltDataDAL as TiltDataDAL
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

def GetTiltBrewData(tiltBrewId, date):
    
    currentTiltBrew = TiltBrewDAL.getTiltBrew(tiltBrewId)
    
    if currentTiltBrew.TiltBrewId > 0:
        allData = {}

        endTime = datetime.now()

        if currentTiltBrew.EndDate:
            endTime = currentTiltBrew.EndDate
        
        allData['duration'] = currentTiltBrew.Duration
        allData['startDate'] = currentTiltBrew.StartDate.strftime(dateFormatString)
        allData['currentDT'] = datetime.now()
        
        allData['tempTarget'] = GenerateTargetData(currentTiltBrew.StartDate, endTime, currentTiltBrew.TempTarget)
        allData['gravityTarget'] = GenerateTargetData(currentTiltBrew.StartDate, endTime, currentTiltBrew.GravityTarget)
        currentDate = endTime
        allData['lastUpdate'] = currentDate.strftime(dateFormatString)
        
        datas = []
        
        if date:
            datas = TiltDataDAL.getDataForTiltBrew(currentTiltBrew.TiltBrewId, date)
        else:
            datas = TiltDataDAL.getDataForTiltBrew(currentTiltBrew.TiltBrewId)
        
        temps1 = []
        gravities = []
        
        # get current datas from the first item in the list
        if len(datas) > 0:
            currentData = datas[-1]  # last in the list
            allData['TempCurrent'] = '{0:.2f}'.format(currentData.Temp)
            allData['GravityCurrent'] = '{0:.3f}'.format(currentData.Gravity)
            allData['LastDataStatus'] = (currentDate - currentData.EventDate).total_seconds() < 120
            allData['LastDataUpdate'] = currentData.EventDate.strftime(dateFormatString)
            
        for x in datas:
            formattedDate = x.EventDate.strftime(dateFormatString)
            temp = {}
            temp['x'] = formattedDate
            temp['y'] = x.Temp
            temps1.append(temp)

            gravity = {}
            gravity['x'] = formattedDate
            gravity['y'] = x.Gravity
            gravities.append(gravity)
            
        allData['Temp'] = temps1
        allData['Gravity'] = gravities
        
        return jsonify(allData)

    return jsonify('')

# def ProcessSubscriptions(TiltBrewId)
