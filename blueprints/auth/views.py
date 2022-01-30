'''
Created on May 17, 2020

@author: justin
'''
from sanic.blueprints import Blueprint
from sanic.response import json

from db.base import get_async_session
from db.auth import User
from sanic_jwt.decorators import protected
from utils.forms import parse_body

bp = Blueprint("auth", url_prefix="auth/")


@bp.route("create_user", methods=["GET", "POST"])
async def create_user(request):

    if request.method == "POST":
        data = parse_body(request)

        async with get_async_session() as session:
            resp = await User.add_user(session, data)

        return json(resp)

    else:
        return json({"ok": False, "msg": "GET not supported"})


@bp.route("logout")
async def logout(request):
    """
    logs a user out
    """
    pass


@bp.route("login_check")
@protected()
async def loggedin(request):
    return json({"ok": True, "msg": "you are logged in"})
