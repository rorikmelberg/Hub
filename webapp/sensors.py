import os
import functools
from webapp.db import get_db
import webapp.DAL.SensorDAL as SensorDAL
import webapp.DAL.SensorDataDAL as SensorDataDAL
import webapp.SMSession as SMSession
import simplejson as json

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import Flask, render_template, session
from flask import jsonify
from flask_session.__init__ import Session
from datetime import datetime

dateFormatString = '%Y-%m-%d %H:%M:%S.%f'

bp = Blueprint('sensors', __name__, url_prefix='/sensors')

@bp.route('/')
@bp.route('/index')
def index():
    sensors = SensorDAL.getValues()
    return render_template('sensors/index.html', sensors = sensors, 
                                            currentDT=datetime.now())

@bp.route('/setdata', methods=['POST']) 
def SetSensorData():
    data = request.json
    
    sensorId = data['SensorId']
    value = data['Value']
    
    # print('{0} - {1}'.format(sensorId, value))
    SensorDataDAL.setValue(sensorId, value)

    return jsonify({"Status":"OK"})
