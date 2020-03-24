import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from datetime import datetime

import webapp.db as wadb
import webapp.DateHelpers as dh

class CurrentData:
    def __init__(self):
        self.CurrentDataId = 0
        self.Name = ''
        self.Value = ''
        self.LastUpdated = ''
    
    def toString(self):
        print('CurrentData: CurrentDataId: {0}, Name: {1}, Value: {2}, LastUpdated: {3}, '.format(self.CurrentDataId, self.Name, self.Value, self.LastUpdated))

def getValues():
    db = wadb.get_db()

    rtn = db.execute('SELECT CurrentDataId, Name, Value, LastUpdated '
                        'FROM CurrentData').fetchall()

    values = []

    for x in rtn:
        values.append(objectify(x))
        
    return values

def setValue(name, value):
    db = wadb.get_db()

    rtn = db.execute('SELECT CurrentDataId, Name, Value, LastUpdated '
                        'FROM CurrentData').fetch()
    if(rtn):
        rtn = db.execute('UPDATE CurrentData '
                            'Value = {0},
                            'LastUpdated = {1}'
                        'WHERE CurrentDataId = {2}', ).fetchall()



    rtn = db.execute('SELECT CurrentDataId, Name, Value, LastUpdated '
                        'FROM CurrentData').fetchall()

    values = []

    for x in rtn:
        values.append(objectify(x))
        
    return values

def objectify(currentData):
    out = CurrentData()
    out.CurrentDataId = currentData[0]
    out.Name = currentData[1]
    out.Value = currentData[2]
    out.LastUpdated = currentData[3]
    return out
