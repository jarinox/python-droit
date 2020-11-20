# main.py - plugins.output - EVAL.session plugin for python-droit
# Copyright 2020 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)


def activateByUsername(data, db):
    if(db.sessions):
        db.sessions.activateByUsername(data[0])
    return "", db

def activateById(data, db):
    if(db.sessions):
        db.sessions.activateById(data[0])
    return "", db

def saveSessions(data, db):
    if(db.sessions):
        db.sessions.saveSessions()
    return "", db

def getUsername(data, db):
    if(db.sessions):
        if(db.sessions.getActive()):
            return db.sessions.getActive().username, db
        else:
            return "", db
    else:
        return "", db

def setDroitname(data, db):
    db.sessions.droitname = data[0]
    return "", db

def setUsername(data, db):
    try:
        active = db.sessions.getActive()
        active.username = data[0]
        active.userData["customUsername"] = True
        db.session.setActive(active)
    except:
        pass
    return "", db