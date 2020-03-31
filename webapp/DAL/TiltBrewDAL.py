import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
import webapp.DateHelpers as dh
import webapp.db as wadb

from datetime import datetime

dateFormatter = '%m/%d/%Y - %H:%M:%S'

class TiltBrew:
    def __init__(self):
        self.TiltBrewId = 0
        self.Title = ''
        self.StartDate = ''
        self.EndDate = ''
        self.StartFormatted = ''
        self.EndFormatted = ''
        self.TempTarget = 0
        self.GravityTarget = 0
        self.Duration = ''

def getCurrentTiltBrewId():
    db = wadb.get_db()

    rtn = db.execute('SELECT TiltBrewId FROM TiltBrews WHERE EndDate is null').fetchone()
    
    if rtn is not None:
        return rtn[0]
    else:
        return 0

def getTiltBrew(tiltBrewId):
    db = wadb.get_db()
    
    tiltBrewRtn = db.execute('SELECT TiltBrewId, Title, StartDate, EndDate, TempTarget, GravityTarget FROM TiltBrews WHERE TiltBrewId = ?', (str(tiltBrewId), )).fetchone()
    
    if tiltBrewRtn:
        tiltBrew = objectifyTiltBrew(tiltBrewRtn)
    else:
        tiltBrew = TiltBrew()
        
    return tiltBrew

def getTiltBrews():
    db = wadb.get_db()

    rtn = db.execute('SELECT TiltBrewId, Title, StartDate, EndDate, TempTarget, GravityTarget FROM TiltBrews').fetchall()
    cooks = []
    
    if rtn is not None:
        for x in rtn:
            cook = objectifyTiltBrew(x)
            cooks.append(cook)
    return cooks

def delete(tiltBrewId):
    db = wadb.get_db()

    rtn = db.execute('DELETE FROM TiltData where TiltBrewId = ?', (tiltBrewId,))
    rtn = db.execute('DELETE FROM TiltBrews where TiltBrewId = ?', (tiltBrewId,))

    db.commit()

def objectifyTiltBrew(tiltBrewList):
    tiltBrew = TiltBrew()
    
    tiltBrew.TiltBrewId = tiltBrewList[0]
    tiltBrew.Title = tiltBrewList[1]
    tiltBrew.StartDate = tiltBrewList[2]
    tiltBrew.EndDate = tiltBrewList[3]
    tiltBrew.TempTarget = tiltBrewList[4]
    tiltBrew.GravityTarget = tiltBrewList[5]
    tiltBrew.StartFormatted = tiltBrew.StartDate.strftime(dateFormatter)
    
    if tiltBrew.EndDate:
        fromTime = tiltBrew.EndDate
        tiltBrew.EndFormatted = tiltBrew.EndDate.strftime(dateFormatter)
    else:
        fromTime = datetime.now()
        tiltBrew.EndFormatted = 'Running'

    calcDuration = (fromTime - tiltBrew.StartDate)
    tiltBrew.Duration = dh.printNiceTimeDelta(calcDuration)
    return tiltBrew

def startTiltBrew(title, tempTarget, gravityTarget):
    db = wadb.get_db()
    
    db.execute('INSERT INTO TiltBrews (Title, StartDate, TempTarget, GravityTarget) VALUES(?,?,?,?)', (title, datetime.now(), tempTarget, gravityTarget,))
    db.commit()

def endCurrentTiltBrew():
    db = wadb.get_db()
    db.execute('UPDATE TiltBrews SET EndDate = ? where EndDate is NULL', (datetime.now(),))
    db.commit()

def update(tiltBrew):
    db = wadb.get_db()
    db.execute('UPDATE TiltBrews '
                    'SET Title = ?, '
                    'TempTarget = ?, '
                    'GravityTarget = ?, '
                'WHERE TiltBrewId = ?', (tiltBrew.Title, tiltBrew.TempTarget, tiltBrew.GravityTarget,))
    db.commit()

if __name__ == "__main__":
    startTiltBrew('TestTitle', 123, 123)
    newTiltBrew = getCurrentTiltBrewId()
    print(newCook)