from flask import session

def setCookId(cookId):
    session['CookId'] = cookId

def getCookId():
    cookId = session.get('CookId', 0)
    return cookId

def setBrewId(BrewId):
    session['BrewId'] = BrewId

def getBrewId():
    brewId = session.get('BrewId', 0)
    return brewId