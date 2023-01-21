import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
import datetime
from flask import current_app

from . import SensorDAL
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

def getLast(sensorId):
    try:
        db = wadb.get_db()

        sql = '''SELECT SensorDataId, SensorId, ValueFloat, ValueChar, EventDate
                            FROM SensorData
                            WHERE SensorId = ?
                            ORDER BY EventDate DESC
                            LIMIT 1'''
        
        rtn = db.execute(sql, (sensorId,)).fetchone()

        value = objectify(rtn)
        return value
    
    except Exception as ex:
        current_app.logger.error(ex)
        raise ex

def getValues(sensorId, startDate, endDate):
    try:
        current_app.logger.debug('{0} {1} {2}'.format(sensorId, startDate, endDate))
        
        db = wadb.get_db()

        sql = '''SELECT SensorDataId, SensorId, ValueFloat, ValueChar, EventDate
                            FROM SensorData
                            WHERE SensorId = ?
                                AND EventDate >= ?
                                AND EventDate < ?
                            ORDER BY EventDate'''
        
        rtn = db.execute(sql, (sensorId, startDate, endDate)).fetchall()

        values = []

        for x in rtn:
            values.append(objectify(x))
            
        return values
    
    except Exception as ex:
        current_app.logger.error(ex)
        raise ex

def setValue(sensorId, value):
    db = wadb.get_db()
    currentTime = datetime.datetime.now()
    
    try:
        sensor = SensorDAL.getValue(sensorId)
        
        # Determines if the data should be rewritten 1 sec before the new entry, i.e. setpoints
        repeatValue = sensor.Type == 'S'
        
        sensorValue = getLast(sensorId)
        
        writeData = True

        if sensorValue.ValueFloat == value:
            writeData = False
            sql = '''UPDATE SensorData
                        SET EventDate = ?
                        WHERE SensorDataId = ?;'''

            rtn = db.execute(sql, (datetime.datetime.now(), sensorValue.SensorDataId, ))
            db.commit()
        
        if repeatValue:
            oneSecAgo = currentTime - datetime.timedelta(seconds=1)
            db.execute('INSERT INTO SensorData (SensorId, ValueFloat, EventDate) VALUES(?, ?, ?)', (sensorId, sensorValue.ValueFloat, oneSecAgo, ))    

        if writeData:
            currentTime = datetime.datetime.now()

            db.execute('INSERT INTO SensorData (SensorId, ValueFloat, EventDate) VALUES(?, ?, ?)', (sensorId, value, currentTime, ))
            db.commit()
    
    except Exception as ex:
        current_app.logger.error(ex)
        raise ex

def objectify(currentData):
    try:
        out = SensorData()
        out.SensorDataId = currentData[0]
        out.SensorId = currentData[1]
        out.ValueFloat = currentData[2]
        out.ValueChar = currentData[3]
        out.EventDate = currentData[4]
        return out
    except Exception as ex:
        current_app.logger.error(ex)
        raise ex

