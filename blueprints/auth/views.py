'''
Created on May 17, 2020

@author: justin
'''
from sanic.blueprints import Blueprint
from sanic.response import json

from utils.auth import authenticate, logout as logout_, is_authenticated
from utils.redis import RedisStore
from utils.forms import parseForm


bp = Blueprint("auth", url_prefix="api/auth/")


@bp.route("createUser", methods=["GET", "POST"])
async def createUser(request):

    if request.method == "POST":

        data = parseForm(request)
        
        print(data)

    return json({"ok:": True})


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
    elif authenticate("", "", dataStore):
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
@is_authenticated
async def loggedin(request):
    return json({"ok": True, "msg": "you are logged in"})
