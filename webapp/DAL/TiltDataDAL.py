import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from datetime import datetime

import webapp.db as wadb
import webapp.DateHelpers as dh

class TiltData:
    def __init__(self):
        self.TiltDataId = 0
        self.EventDate = ''
        self.Temp = ''
        self.Gravity = ''
        self.BrewId = 0
    
    def toString(self):
        print('TiltDataId: {0}, EventDate: {1}, Temp: {2}, Gravity: {3}, BrewId: {5}'.format(self.TiltDataId, self.EventDate, self.Temp, self.Gravity, self.TempBrewId))

def getDataForBrew(brewId, dateSince = None):
    db = wadb.get_db()

    if dateSince == None:
        rtn = db.execute('SELECT TiltDataId, EventDate, Temp, Gravity, BrewId '
                        'FROM TiltData WHERE BrewId = ? ', (brewId,)).fetchall()
    else:
        rtn = db.execute('SELECT TiltDataId, EventDate, Temp, Gravity, BrewId '
                        'FROM TiltData WHERE BrewId = ? '
                        '  AND EventDate > ?', (brewId, dateSince)).fetchall()

    datas = []

    for row in rtn:
        data = objectify(row)
        datas.append(data)

    return datas

def getLastDataForBrew(brewId):
    db = wadb.get_db()

    rtn = db.execute('SELECT TiltDataId, EventDate, Temp, Gravity, BrewId '
                        'FROM TiltData WHERE BrewId = ? '
                        'ORDER BY EventDate DESC '
                        'LIMIT 1', (brewId,)).fetchone()
    
    if rtn:
        tiltData = objectify(rtn)
    else:
        tiltData = TiltData()

    return tiltData

def objectify(row):
    data = TiltData()
    data.TiltDataId = int(row[0])
    data.EventDate = dh.convertTime(row[1])
    data.Temp = float('{0:.2f}'.format(row[2]))
    data.Gravity = float('{0:.4f}'.format(row[3]))
    data.BrewId = row[4]
    return data    

def logTemps(temp, gravity, brewId):
    db = wadb.get_db()

    rtn = db.execute('SELECT TiltDataId, Temp, Gravity FROM TiltData ORDER BY EventDate DESC LIMIT 1').fetchall()
    if rtn[0][1] != temp or rtn[0][2] != gravity:
        db.execute('INSERT INTO TiltData (EventDate, Temp, Gravity, BrewId) VALUES(?, ?, ?, ?)', (datetime.now(), temp, gravity, brewId, ))
        db.commit()
    else:
        db.execute('UPDATE TiltData SET EventDate = ? WHERE TiltDataId = ?', (datetime.now(), rtn[0][0], ))
        db.commit()

if __name__ == "__main__":
    getDataForBrew(1)