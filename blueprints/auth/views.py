'''
Created on May 17, 2020

@author: justin
'''
from sanic.blueprints import Blueprint
from sanic.response import json

from utils.auth import checkCredentials, logout as logout_, isAuthenticated
from utils.redis import RedisStore
from db.base import getSession
from db.appTables import User
from utils.auth import createUser as createUser_
from blueprints.auth.forms import UserForm, LoginForm

bp = Blueprint("auth", url_prefix="api/auth/")


@bp.route("createUser", methods=["GET", "POST"])
async def createUser(request):

    if request.method == "POST":

        result = {}
        form = UserForm(request)
#         print("validate form", form.validate())
#         print("errors", form.errors)
#         print("form", dir("form"))

        dSession = getSession()

        # Make this faster later
        unameResult = dSession.query(User.id).filter(User.username == form.data["username"]).scalar()
        emailResult = dSession.query(User.id).filter(User.email == form.data["email"]).scalar()
        errors = []
        if unameResult:
            errors.append({"msg": "This user already exists"})
        if emailResult:
            errors.append({"msg": "This email already exists"})

        if errors:
            result["errors"] = errors
            result["ok"] = False
        else:
            createUser_(form.data, dSession)
            result["ok"] = True

        return json(result)

    else:
        form = UserForm(request)
        return json({"csrf_token": form.csrf_token._value()})
#         return json({"csrf_token:": form._csrf.session["csrf"]})


@bp.route("login", methods=["GET", "POST"])
async def login(request):
    """
    logs a user in
    """

    if request.method == "POST":
        dataStore = RedisStore(request)

        form = LoginForm(request)
        if not form.validate():
            return json({"ok": False, "errors": form.errors})

        ident = form.data["ident"]
        password = form.data["password"]
        username = checkCredentials(ident, password)
        # here we check the backend to see that the user is authenticated
        # writing the state in the user cookie is just a courtesy
        if dataStore.session.get("authenticated"):
            return json({"ok": False, "msg": "please log out before logging in"})

        elif username:
            response = json({"ok": True})
            response.cookies["authenticated"] = "true"
            response.cookies["authenticated"]["samesite"] = "Strict"
            request.ctx.session["username"] = username
            return response
        else:
            return json({"ok": False, "msg": "login or password incorrect"})
    else:
        return json({"ok": False, "msg": "please post the appropriate data"})


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
