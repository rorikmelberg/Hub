import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import webapp.DateHelpers as dh
import webapp.db as wadb
from . import SensorDataDAL

from datetime import datetime

dateFormatter = '%m/%d/%Y - %H:%M:%S'

class Brew:
    def __init__(self):
        self.BrewId = 0
        self.Title = ''
        self.StartDate = ''
        self.EndDate = ''
        self.TempSensorId = 0
        self.TempTargetSensorId = 0
        self.GravitySensorId = 0
        self.GravTargetSensorId = 0
        self.StartFormatted = ''
        self.EndFormatted = ''
        self.TempTarget = 0
        self.GravityTarget = 0
        self.Duration = ''
        self.BrewRunning = False

def getCurrentBrewId():
    db = wadb.get_db()

    rtn = db.execute('SELECT BrewId FROM Brews WHERE EndDate is null').fetchone()
    
    if rtn is not None:
        return rtn[0]
    else:
        return 0

def getBrew(brewId):
    db = wadb.get_db()
    
    sql = '''SELECT BrewId, 
                Title, 
                StartDate, 
                EndDate, 
                TempSensorId,
                TempTargetSensorId,
                GravitySensorId,
                GravTargetSensorId
            FROM Brews WHERE BrewId = ?'''

    brewRtn = db.execute(sql, (str(brewId), )).fetchone()
    
    if brewRtn:
        brew = objectifyBrew(brewRtn)

        # Lookup Temp and Grav 

        brew.TempTarget = SensorDataDAL.getLast(brew.TempTargetSensorId).ValueFloat
        brew.GravityTarget = SensorDataDAL.getLast(brew.GravitySensorId).ValueFloat
    else:
        brew = Brew()
        
    return brew

def getBrews():
    db = wadb.get_db()

    sql = '''SELECT BrewId, 
                Title, 
                StartDate, 
                EndDate, 
                TempSensorId,
                TempTargetSensorId,
                GravitySensorId,
                GravTargetSensorId
            FROM Brews'''

    rtn = db.execute(sql).fetchall()
    brews = []
    
    if rtn is not None:
        for x in rtn:
            brew = objectifyBrew(x)
            brews.append(brew)
    return brews

def delete(brewId):
    db = wadb.get_db()

    rtn = db.execute('DELETE FROM Brews where BrewId = ?', (brewId,))

    db.commit()

def objectifyBrew(brewList):
    brew = Brew()
    
    brew.BrewId = brewList[0]
    brew.Title = brewList[1]
    brew.StartDate = brewList[2]
    brew.EndDate = brewList[3]
    brew.TempSensorId = brewList[4]
    brew.TempTargetSensorId = brewList[5]
    brew.GravitySensorId = brewList[6]
    brew.GravTargetSensorId = brewList[7]

    brew.StartFormatted = brew.StartDate.strftime(dateFormatter)
    
    if brew.EndDate:
        fromTime = brew.EndDate
        brew.EndFormatted = brew.EndDate.strftime(dateFormatter)
        brew.BrewRunning = False
    else:
        fromTime = datetime.now()
        brew.EndFormatted = 'Running'
        brew.BrewRunning = True

    calcDuration = (fromTime - brew.StartDate)
    brew.Duration = dh.printNiceTimeDelta(calcDuration)
    return brew

def startBrew(title, tempTarget, gravityTarget):
    db = wadb.get_db()
    
    sql = '''INSERT INTO Brews (Title, 
                            StartDate, 
                            TempTarget, 
                            GravityTarget,
                            TempSensorId,
                            TempTargetSensorId,
                            GravitySensorId,
                            GravTargetSensorId) 
                            VALUES(?,?,?,?,2,3,4,5)'''

    db.execute(sql, (title, datetime.now(), tempTarget, gravityTarget,))
    db.commit()

def endCurrentBrew():
    db = wadb.get_db()
    db.execute('UPDATE Brews SET EndDate = ? where EndDate is NULL', (datetime.now(),))
    db.commit()

def update(Brew):
    db = wadb.get_db()
    db.execute('UPDATE Brews '
                    'SET Title = ?, '
                    'TempTarget = ?, '
                    'GravityTarget = ?, '
                'WHERE BrewId = ?', (Brew.Title, Brew.TempTarget, Brew.GravityTarget,))
    db.commit()

if __name__ == "__main__":
    startBrew('TestTitle', 123, 123)
    newBrew = getCurrentBrewId()
    print(newBrew)