'''
Created on May 17, 2020

@author: justin
'''
import datetime

from db.auth import User
from db.base import get_async_session
from sanic.blueprints import Blueprint
from sanic.request import Request
from sanic.response import json
from sanic_jwt.decorators import protected
from utils.encrypt import EncryptJson
from utils.forms import parse_body

bp = Blueprint("auth", url_prefix="api/auth/")


@bp.route("add_user", methods=["GET", "POST"])
async def add_user(request: Request):

    if request.method == "POST":
        data = parse_body(request)

        async with get_async_session() as session:
            resp = await User.add_user(session, data)
        return json(resp)

    else:
        return json({"ok": False, "msg": "GET not supported"})


@bp.route("verify_user", methods=["GET"])
async def verify_user(request: Request):
    args = request.get_args()
    if "token" in args:
        e = EncryptJson()
        resp = e.decrypt(args.get("token"))
        if resp["expiry"] > datetime.datetime.utcnow().timestamp():
            async with get_async_session() as session:
                await User.verify_user(session, resp["email"])
                return json({"ok": True})
    return json({"ok": False})


@bp.route("verify_new_email", methods=["GET"])
async def verify_new_email(request: Request):
    args = request.get_args()
    if "token" in args:
        e = EncryptJson()
        resp = e.decrypt(args["token"])
        if resp["expiry"] > datetime.datetime.utcnow().timestamp():
            async with get_async_session() as session:
                await User.update_email(session, resp["old_email"], resp["new_email"])
                return json({"ok": True})
    return json({"ok": False})


@bp.route("verify_reset_password", methods=["GET"])
async def verify_reset_password(request: Request):
    return json({"ok": True})


@bp.route("logout")
async def logout(request: Request):
    response = json({"ok": True})
    response.cookies.pop("access_token", None)
    response.cookies.pop("access_token_signature", None)
    return response


@bp.route("login_check")
@protected()
async def loggedin(request: Request):
    return json({"ok": True, "msg": "you are logged in"})
