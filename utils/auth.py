'''
Created on May 17, 2020

@author: justin

tools for authentication
'''
from sanic.response import json
from sqlalchemy.sql import or_

from db.appTables import User
from db.base import getSession
from db.utils import bulkInsert
from settingsManager import settingsManager
from utils.redis import RedisStore


def checkCredentials(username, password, redisStore, dSession=None):
    """
    if the authentication info is ok
    then sets the authentication to authenticated

    """

    dSession = dSession or getSession()
    user = dSession.query(User).filter(User.username == username)
    if user and user.password == password or redisStore.session["authenticated"]:
        return True
    else:
        return False


def login(request, response):
    """
    request = to set the value in the cookie
    response = the response object to set the cookie
    sets the state in redis that the user
    is logged in
    """

    response.cookies["authenticated"] = True
    request.ctx.session["session"]


def logout(request):
    """
    performs a logout on the request
    """

    dataStore = RedisStore(request)
    if dataStore.session.get("authenticated"):
        response = json({"ok": True})
        del dataStore.session["authenticated"]
        del response.cookies["authenticated"]
        return response
    else:
        return json({"ok": False, "msg": "not logged in"})


def isAuthenticated(f):
    """
    decorator for authentication
    decorates a view
    """

    def func(request):

        dataStore = RedisStore(request)
        if dataStore.session.get("authenticated"):
            return f(request)
        else:
            return json({"ok": False, "msg": "please authenticate"})

    return func


def createUser(data, dSession=None):
    """
    creates a user
    """
    dSession = getSession(session=dSession)
    bulkInsert(dSession, User, [data])


def deleteUser(info, dSession=None):
    """
    deletes a user
    """
    dSession = getSession(session=dSession)
    query = User.__table__.delete().where(or_(User.username == info,
                                              User.email == info))
    dSession.execute(query)
    dSession.commit()


def userExists(info, dSession=None):

    dSession = getSession(session=dSession)
    uid = dSession.query(User.id).filter(or_(User.username == info,
                                             User.email == info)).\
        scalar()

    return True if uid else False
