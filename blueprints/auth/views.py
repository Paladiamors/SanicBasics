'''
Created on May 17, 2020

@author: justin
'''
from sanic.blueprints import Blueprint
from sanic.response import json

from utils.auth import checkCredentials, logout as logout_, isAuthenticated
from utils.redis import RedisStore
from utils.forms import parseForm
from settingsManager import settingsManager
from db.base import getSession
from db.appTables import User
from sqlalchemy.sql import or_

env = settingsManager.getSetting("ENV")
bp = Blueprint("auth", url_prefix="api/auth/")


@bp.route("createUser", methods=["GET", "POST"])
async def createUser(request):

    if request.method == "POST":

        result = {}
        data = parseForm(request)
        dSession = getSession(env)

        unameResult = dSession(User.id).filter(User.username == data["username"])
        emailResult = dSession(User.id).filter(User.email == data["email"])

        errors = []
        if unameResult:
            errors.append({"msg": "This user already exists"})
        if emailResult:
            errors.append({"msg": "This email already exists"})

        if errors:
            result["errors"] = errors
            result["ok"] = False
        else:

            result["ok"] = True

        return json(result)

    else:
        return json({"errors:": [{"msg": "Please post the appropriate data"}]})


@bp.route("login")
async def login(request):
    """
    logs a user in
    """
    dataStore = RedisStore(request)

    # here we check the backend to see that the user is authenticated
    # writing the state in the user cookie is just a courtesy
    if dataStore.session.get("authenticated"):
        return json({"ok": False, "msg": "please log out before logging in"})
    elif checkCredentials("", "", dataStore):
        response = json({"ok": True})
        response.cookies["authenticated"] = "True"
        response.cookies["authenticated"]["samesite"] = "Strict"
        return response
    else:
        return json({"ok": False, "msg": "login or password incorrect"})


@bp.route("logout")
async def logout(request):
    """
    logs a user out
    """
    return logout_(request)


@bp.route("login_check")
@isAuthenticated
async def loggedin(request):
    return json({"ok": True, "msg": "you are logged in"})
