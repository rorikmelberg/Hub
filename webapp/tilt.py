import os
import functools
from webapp.db import get_db
import webapp.DAL.TiltBrewDAL as TiltBrewDAL
import webapp.DAL.TiltDataDAL as TiltDataDAL
import webapp.DAL.SubscriptionDL as SubscriptionDL
import webapp.BO.TiltBrewBO as TiltBrewBO
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

bp = Blueprint('tilt', __name__, url_prefix='/tilt')

@bp.route('/')
@bp.route('/index')
def index():
    tiltBrewId = SMSession.getTiltBrewId()
    
    if tiltBrewId == 0:
        tiltBrewId = TiltBrewDAL.getCurrentTiltBrewId()
        SMSession.setTiltBrewId(tiltBrewId)
    
    currentTiltBrew = TiltBrewDAL.getTiltBrew(tiltBrewId)

    return render_template('tilt/index.html', tiltBrew = currentTiltBrew, 
                                            currentDT=datetime.now())

@bp.route('/editbrew', methods=['GET', 'POST'])
def editbrew():
    currentTiltBrewId = TiltBrewDAL.getCurrentTiltBrewId()

    if request.method == "POST":
        if currentTiltBrewId == 0:
            title = request.form["title"]
            tempTarget =  request.form["tempTarget"]
            gravityTarget =  request.form["gravityTarget"]
            
            TiltBrewDAL.startTiltBrew(title, tempTarget, gravityTarget)
            tiltBrewId = TiltBrewDAL.getCurrentTiltBrewId()
            SMSession.setTiltBrewId(tiltBrewId)
        else:
            TiltBrewDAL.endCurrentTiltBrew()    
        
        return redirect(url_for('tilt.index'))

    else:
        tiltBrew = TiltBrewDAL.getTiltBrew(currentTiltBrewId)
        title = tiltBrew.Title
        return render_template('tilt/editbrew.html', tiltBrew = tiltBrew)

@bp.route('/selectbrew', methods=['GET']) 
def selectTiltBrew():
    tiltBrewId = request.args.get('tiltBrewId')

    if tiltBrewId:
        SMSession.setTiltBrewId(tiltBrewId)
        return redirect(url_for('tilt.index'))

    else:
        tiltBrews = TiltBrewDAL.getTiltBrews()
        return render_template('tilt/selectbrew.html', tiltBrews=tiltBrews)

@bp.route('/deletebrew', methods=['GET']) 
def deleteBrew():
    
    tiltBrewId = request.args.get('tiltBrewId')
    TiltBrewDAL.delete(tiltBrewId)
    return redirect(url_for('selectCook'))

@bp.route('/getdata', methods=['GET']) 
def GetTiltBrewData():
    date = request.args.get('lastUpdate')
    tiltBrewId = request.args.get('tiltBrewId')

    return TiltBrewBO.GetTiltBrewData(tiltBrewId, date)

@bp.route('/setdata', methods=['POST']) 
def SetTiltBrewData():
    print(request.json)
    datas = json.loads(request.json)
    tiltBrewId = TiltBrewDAL.getCurrentTiltBrewId()
    
    if(tiltBrewId > 0):
        TiltDataDAL.logTemps(datas[0], datas[1], tiltBrewId)

    return jsonify({"Status":"OK"})