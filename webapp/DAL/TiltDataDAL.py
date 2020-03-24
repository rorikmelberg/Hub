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
        self.TiltBrewId = 0
    
    def toString(self):
        print('TiltDataId: {0}, EventDate: {1}, Temp: {2}, Gravity: {3}, TiltBrewId: {5}'.format(self.TiltDataId, self.EventDate, self.Temp, self.Gravity, self.TempBrewId))

def getDataForTiltBrew(tiltBrewId, dateSince = None):
    db = wadb.get_db()

    if dateSince == None:
        rtn = db.execute('SELECT TiltDataId, EventDate, Temp, Gravity, TiltBrewId '
                        'FROM TiltData WHERE TiltBrewId = ? ', (tiltBrewId,)).fetchall()
    else:
        rtn = db.execute('SELECT TiltDataId, EventDate, Temp, Gravity, TiltBrewId '
                        'FROM TiltData WHERE TiltBrewId = ? '
                        '  AND EventDate > ?', (tiltBrewId, dateSince)).fetchall()

    datas = []

    for x in rtn:
        data = TiltData()
        data.TiltDataId = x[0]
        data.EventDate = dh.convertTime(x[1])
        data.Temp = float('{0:.2f}'.format(x[2]))
        data.Gravity = float('{0:.4f}'.format(x[3]))
        data.TiltBrewId = x[4]
        
        datas.append(data)

    return datas

def logTemps(temp, gravity, tiltBrewId):
    db = wadb.get_db()

    rtn = db.execute('SELECT TiltDataId, Temp, Gravity FROM TiltData ORDER BY EventDate DESC LIMIT 1').fetchall()
    if rtn[0][1] != temp or rtn[0][2] != gravity:
        db.execute('INSERT INTO TiltData (EventDate, Temp, Gravity, TiltBrewId) VALUES(?, ?, ?, ?)', (datetime.now(), temp, gravity, tiltBrewId, ))
        db.commit()
    else:
        db.execute('UPDATE TiltData SET EventDate = ? WHERE TiltDataId = ?', (datetime.now(), rtn[0][0], ))
        db.commit()

if __name__ == "__main__":
    getDataForTiltBrew(1)