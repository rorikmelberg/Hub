import os
import functools
from webapp.db import get_db
import webapp.DAL.BrewDAL as BrewDAL
import webapp.DAL.SensorDataDAL as DataDAL
import webapp.DAL.SubscriptionDL as SubscriptionDL
import webapp.BO.BrewBO as BrewBO
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

bp = Blueprint('brew', __name__, url_prefix='/brew')

@bp.route('/')
@bp.route('/index')
def index():
    brewId = SMSession.getBrewId()
    
    if brewId == 0:
        brewId = BrewDAL.getCurrentBrewId()
        SMSession.setBrewId(brewId)
    
    currentBrew = BrewDAL.getBrew(brewId)

    return render_template('brew/index.html', brew = currentBrew, 
                                            currentDT=datetime.now())

@bp.route('/editbrew', methods=['GET', 'POST'])
def editbrew():
    currentBrewId = BrewDAL.getCurrentBrewId()

    if request.method == "POST":
        if currentBrewId == 0:
            title = request.form["title"]
            tempTarget =  request.form["tempTarget"]
            gravityTarget =  request.form["gravityTarget"]
            
            BrewDAL.startBrew(title, tempTarget, gravityTarget)
            brewId = BrewDAL.getCurrentBrewId()
            SMSession.setBrewId(brewId)
        else:
            BrewDAL.endCurrentBrew()    
        
        return redirect(url_for('brew.index'))

    else:
        brew = BrewDAL.getBrew(currentBrewId)
        title = brew.Title
        return render_template('brew/editbrew.html', brew = brew)

@bp.route('/selectbrew', methods=['GET']) 
def selectBrew():
    brewId = request.args.get('brewId')

    if brewId:
        SMSession.setBrewId(brewId)
        return redirect(url_for('brew.index'))

    else:
        brews = BrewDAL.getBrews()
        return render_template('brew/selectbrew.html', brews=brews)

@bp.route('/deletebrew', methods=['GET']) 
def deleteBrew():
    
    brewId = request.args.get('brewId')
    BrewDAL.delete(brewId)
    return redirect(url_for('selectCook'))

@bp.route('/getdata', methods=['GET']) 
def GetBrewData():
    date = request.args.get('lastUpdate')
    brewId = request.args.get('brewId')
    print(brewId)
    return BrewBO.GetBrewData(brewId, date)

# @bp.route('/setdata', methods=['POST']) 
# def SetBrewData():
#     print(request.json)
#     datas = json.loads(request.json)
#     brewId = BrewDAL.getCurrentBrewId()
#     
#     if(brewId > 0):
#         temp
#         TiltDataDAL.logTemps(datas[0], datas[1], brewId)
# 
#     return jsonify({"Status":"OK"})