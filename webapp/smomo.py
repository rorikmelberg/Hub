import os
import functools
from webapp.db import get_db
import webapp.DAL.CookDL as CookDL
import webapp.DAL.TempDL as TempDL
import webapp.DAL.SubscriptionDL as SubscriptionDL
import webapp.BO.CookBO as CookBO
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

bp = Blueprint('smomo', __name__, url_prefix='/smomo')

@bp.route('/')
@bp.route('/index')
def index():
    cookId = SMSession.getCookId()
    
    if cookId == 0:
        cookId = CookDL.getCurrentCookId()
        SMSession.setCookId(cookId)
    
    currentCook = CookDL.getCook(cookId)

    latestTime = datetime(2019,1,1)
    latestTemp = [0, 0, 0]
    minTemp = [9999, 9999, 9999]
    maxTemp = [0, 0, 0]
    temps = []

    if currentCook.CookId > 0:
        temps = TempDL.getTempsForCook(currentCook.CookId)

        for x in temps:
            if x.EventDate > latestTime:
                latestTime = x.EventDate
                latestTemp[0] = x.Temp1
                latestTemp[1] = x.Temp2
                latestTemp[2] = x.Temp3
            """
            if x.Temp < minTemp[x.SensorNum]:
                minTemp[x.SensorNum] = x.Temp
            
            if x.Temp > maxTemp[x.SensorNum]:
                maxTemp[x.SensorNum] = x.Temp
            """
            
    return render_template('smomo/index.html', cook = currentCook, 
                                            latestTime = latestTime,
                                            latestTemp = latestTemp,
                                            minTemp = minTemp,
                                            maxTemp = maxTemp,
                                            temps = temps,
                                            values = temps,
                                            currentDT=datetime.now())

@bp.route('/editcook', methods=['GET', 'POST'])
def editcook():
    currentCookId = CookDL.getCurrentCookId()

    if request.method == "POST":
        if currentCookId == 0:
            title = request.form["title"]
            smokerTarget =  request.form["smokerTarget"]
            target =  request.form["target"]
            CookDL.startCook(title, smokerTarget, target)
            cookId = CookDL.getCurrentCookId()
            SMSession.setCookId(cookId)
        else:
            CookDL.endCurrentCook()    
        
        return redirect(url_for('smomo.editcook'))

    else:
        cook = CookDL.getCook(currentCookId)
        subs = SubscriptionDL.getSubscriptionsForCook(currentCookId)
        title = cook.Title
        return render_template('smomo/editcook.html', cook = cook,
                                                subs = subs)

@bp.route('/addsubscription', methods=['POST'])
def addsubscription():
    email = request.form["Email"]
    cookId = request.form["CookId"]
    SubscriptionDL.insertSubscription(cookId, email)
    return redirect(url_for('smomo.editcook'))

@bp.route('/deletesub', methods=['GET'])
def deletesubscription():
    subscriptionId = request.args.get('subscriptionId')
    SubscriptionDL.delete(subscriptionId)
    return redirect(url_for('smomo.editcook'))

@bp.route('/selectcook', methods=['GET']) 
def selectCook():
    cookId = request.args.get('cookId')

    if cookId:
        SMSession.setCookId(cookId)
        return redirect(url_for('smomo.index'))

    else:
        cooks = CookDL.getCooks()
        return render_template('smomo/selectcook.html', cooks=cooks)

@bp.route('/deletecook', methods=['GET']) 
def deleteCook():
    
    cookId = request.args.get('cookId')
    CookDL.delete(cookId)
    return redirect(url_for('selectCook'))

@bp.route('/getdata', methods=['GET']) 
def GetCookData():
    date = request.args.get('lastUpdate')
    forceUpdate = request.args.get('forceUpdate')
    cookId = request.args.get('cookId')

    # Remmed out because force data isn't available
    # if(forceUpdate):
    #    RecordData()

    return CookBO.GetCookData(cookId, date)

@bp.route('/setdata', methods=['POST']) 
def SetCookData():
    temps = json.loads(request.json)
    cookId = CookDL.getCurrentCookId()
    print(cookId)
    print(temps)

    if(cookId > 0):
        TempDL.logTemps(temps, cookId)

    return jsonify({"Status":"OK"})