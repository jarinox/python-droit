# main.py - plugins.output - EVAL.session plugin for python-droit
# Copyright 2020-2021 - Jakob Stolze
#
# This file is part of python-droit (https://github.com/jarinox/python-droit)


def activateByUsername(data, variables, db):
    if(db.sessions):
        db.sessions.activateByUsername(data[0])
    return "", variables, db

def activateById(data, variables, db):
    if(db.sessions):
        db.sessions.activateById(data[0])
    return "", variables, db

def saveSessions(data, variables, db):
    if(db.sessions):
        db.sessions.saveSessions()
    return "", variables, db

def getUsername(data, variables, db):
    if(db.sessions):
        if(db.sessions.getActive()):
            return db.sessions.getActive().username, variables, db
        else:
            return "", variables, db
    else:
        return "", variables, db

def setDroitname(data, variables, db):
    db.sessions.droitname = data[0]
    return "", variables, db

def setUsername(data, variables, db):
    try:
        active = db.sessions.getActive()
        active.username = data[0]
        active.userData["customUsername"] = True
        db.session.setActive(active)
    except:
        pass
    return "", variables, db