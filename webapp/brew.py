import os
import functools
import sys
from datetime import datetime
from datetime import timedelta
import requests

from db import get_db
import DAL.BrewDAL as BrewDAL
import DAL.SensorDataDAL as DataDAL
import DAL.SubscriptionDL as SubscriptionDL
import BO.BrewBO as BrewBO
import SMSession as SMSession
import simplejson as json

from flask import current_app
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

bp = Blueprint('brew', __name__, url_prefix='/brew')

@bp.route('/')
@bp.route('/chart')
def chart():
    brewId = SMSession.getBrewId()
    
    if brewId == 0:
        brewId = BrewDAL.getCurrentBrewId()
        SMSession.setBrewId(brewId)
    
    currentBrew = BrewDAL.getBrew(brewId)

    return render_template('brew/chart.html', 
                                brew=currentBrew, 
                                currentDT=datetime.now())

@bp.route('/editbrew', methods=['GET', 'POST'])
def editbrew():
    TEMP_SETPOINT_ID = 3
    GRAVITY_SETPOINT_ID = 5
    currentBrewId = BrewDAL.getCurrentBrewId()

    if request.method == "POST":
        if currentBrewId == 0:
            title = request.form["title"]
            tempTarget =  request.form["tempTarget"]
            gravityTarget =  request.form["gravityTarget"]
            
            BrewDAL.startBrew(title, tempTarget, gravityTarget)

            DataDAL.setValue(TEMP_SETPOINT_ID, tempTarget)
            DataDAL.setValue(GRAVITY_SETPOINT_ID, gravityTarget)

            brewId = BrewDAL.getCurrentBrewId()
            SMSession.setBrewId(brewId)
        else:
            BrewDAL.endCurrentBrew()    
        
        return redirect(url_for('brew.chart'))

    else:
        brew = BrewDAL.getBrew(currentBrewId)
        title = brew.Title
        return render_template('brew/editbrew.html', brew = brew)

@bp.route('/selectbrew', methods=['GET']) 
def selectBrew():
    brewId = request.args.get('brewId')

    if brewId:
        SMSession.setBrewId(brewId)
        return redirect(url_for('brew.chart'))

    else:
        brews = BrewDAL.getBrews()
        return render_template('brew/selectbrew.html', brews=brews)

@bp.route('/deletebrew', methods=['GET']) 
def deleteBrew():
    
    brewId = request.args.get('brewId')
    BrewDAL.delete(brewId)
    return redirect(url_for('brew.selectBrew'))

@bp.route('/getdata', methods=['GET']) 
def GetBrewData():
    try:

        date = request.args.get('lastUpdate')
        brewId = request.args.get('brewId')
        current_app.logger.debug('GetBrewData: {} {}'.format(brewId, date))
        return BrewBO.GetBrewData(brewId, date)
    
    except Exception as ex:
        current_app.logger.exception(ex)


@bp.route('/sendBrewFatherData', methods=['GET']) 
def SendBrewFatherData():
    try:
        payload = BrewBO.GetBrew15MinAverage()

        if len(payload) > 0:
            url = 'http://log.brewfather.net/stream?id=6ZOedsVYxefJqx'
            # url = 'http://test.com'
            
            try:
                response = requests.post(url, json=payload, timeout=10)
                
                response.raise_for_status()
                
                response_data = response.json()
                return f'Success! Response data: {response_data}'
            except requests.exceptions.HTTPError as http_err:
                return f'HTTP error occurred: {http_err}'
            except requests.exceptions.RequestException as err:
                return f'An error occurred: {err}'
    except Exception as ex:
        current_app.logger.exception(ex)
        return f'Error: {ex}'
    