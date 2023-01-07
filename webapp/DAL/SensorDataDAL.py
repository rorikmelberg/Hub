import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from datetime import datetime

import webapp.db as wadb
import webapp.DateHelpers as dh

class SensorData:
    def __init__(self):
        self.SensorDataId = 0
        self.SensorId = 0
        self.ValueFloat = 0.0
        self.ValueChar = ''
        self.EventDate = ''

    def toString(self):
        print('SensorData: SensorDataId: {0}, SensorId: {1}, ValueFloat: {2}, ValueChar: {3}, EventDate: {4}, '.format(self.SensorDataId, self.SensorDataId, self.ValueFloat, self.ValueChar, self.EventDate))


def getValues(startDate, endDate):
    db = wadb.get_db()

    sql = '''SELECT SensorDataId, SensorId, ValueFloat, ValueChar, EventDate
                        FROM SensorData
                        WHERE EventDate between {0} and {1}'''.format(startDate, endDate)

    rtn = db.execute(sql).fetchall()

    values = []

    for x in rtn:
        values.append(objectify(x))
        
    return values

def setValue(sensorId, value):
    db = wadb.get_db()

    db.execute('INSERT INTO SensorData (SensorId, ValueFloat, EventDate) VALUES(?, ?, ?)', (sensorId, value, datetime.now(), ))
    db.commit()
    
def objectify(currentData):
    out = SensorData()
    out.SensorDataId = currentData[0]
    out.SensorId = currentData[1]
    out.ValueFloat = currentData[2]
    out.ValueChar = currentData[3]
    out.EventDate = currentData[4]
    return out
