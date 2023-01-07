import sys
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from datetime import datetime

sys.path.append('C:\\Users\\rorik\\OneDrive\\Documents\\GitHub\\Hub')

import webapp.db as wadb
import webapp.DateHelpers as dh

class Sensor:
    def __init__(self):
        self.SensorId = 0
        self.Name = ''
        self.Type = ''
    
    def toString(self):
        print('Sensor: SensorId: {0}, Name: {1}'.format(self.SensorId, self.Name))

def getValues():
    db = wadb.get_db()

    sql = '''SELECT SensorId, Name
                        FROM Sensors'''

    rtn = db.execute(sql).fetchall()

    values = []

    for x in rtn:
        values.append(objectify(x))
        
    return values

def setValue(sensorId, name):
    db = wadb.get_db()

    sql = '''SELECT SensorId, Name 
                FROM Sensors
                WHERE SensorId = {0}'''.format(sensorId)

    rtn = db.execute(sql).fetch()
    if(rtn):
        rtn = db.execute('''UPDATE Sensors
                                SET Name = {1},
                            WHERE CurrentDataId = {0}'''.format(sensorId, name), ).fetchall()
    else:
        rtn = db.execute('''INSERT INTO Sensors (Name)
                                values({0})'''.format(name), ).fetchall()

def objectify(currentData):
    out = Sensor()
    out.SensorId = currentData[0]
    out.Name = currentData[1]
    return out

if __name__ == "__main__":
    rtn = getValues()
    print(rtn)