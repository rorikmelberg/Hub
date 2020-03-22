from flask import session

def setCookId(cookId):
    session['CookId'] = cookId

def getCookId():
    cookId = session.get('CookId', 0)
    return cookId

def setTiltBrewId(tiltBrewId):
    session['TiltBrewId'] = tiltBrewId

def getTiltBrewId():
    tiltBrewId = session.get('TiltBrewId', 0)
    return tiltBrewId