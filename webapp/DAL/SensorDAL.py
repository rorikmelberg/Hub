import sys
import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from datetime import datetime
from flask import current_app

import webapp.db as wadb
import webapp.DateHelpers as dh

class Sensor:
    def __init__(self):
        self.SensorId = 0
        self.Name = ''
        self.Type = ''
    
    def toString(self):
        print('Sensor: SensorId: {0}, Name: {1}, Type {2}'.format(self.SensorId, self.Name, self.Type))

def getValue(sensorId):
    try:
        db = wadb.get_db()

        sql = '''SELECT SensorId, Name, Type
                    FROM Sensors
                    WHERE SensorId = ?'''

        x = db.execute(sql, (sensorId,)).fetchone()
        
        value = objectify(x)
        return value

    except Exception as ex:
        current_app.logger.error(ex)
        raise ex


def getValues():
    try:

        db = wadb.get_db()

        sql = '''SELECT SensorId, Name, Type
                            FROM Sensors'''

        rtn = db.execute(sql).fetchall()

        values = []

        for x in rtn:
            values.append(objectify(x))
            
        return values

    except Exception as ex:
        current_app.logger.error(ex)
        raise ex

def setValue(sensorId, name, type):
    try:
        db = wadb.get_db()
        sensor = getValue(sensorId)

        if(sensor):
            sql = '''UPDATE Sensors
                                    SET Name = ?,
                                        Type = ?
                                WHERE CurrentDataId = ?'''

            rtn = db.execute(sql, (sensorId, name, type)).fetchall()
        else:
            sql = '''INSERT INTO Sensors (Name)
                                    values(?)'''
            rtn = db.execute(sql, (name, )).fetchall()
    
    except Exception as ex:
        current_app.logger.error(ex)
        current_app.logger.info(ex.Message)
        raise ex

def objectify(currentData):
    try:
        out = Sensor()
        out.SensorId = currentData[0]
        out.Name = currentData[1]
        out.Type = currentData[2]
        return out
    except Exception as ex:
        current_app.logger.error(ex)
        raise ex


if __name__ == "__main__":
    rtn = getValues()
    print(rtn)
