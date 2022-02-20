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
from utils.forms import parse_form_or_body

bp = Blueprint("auth", url_prefix="api/auth/")


@bp.route("add_user", methods=("POST", ))
async def add_user(request: Request):

    data = parse_form_or_body(request)
    async with get_async_session() as session:
        resp = await User.add_user(session, data)
    return json(resp)


@bp.route("delete_user", methods=("POST",))
async def delete_user(request):
    # TODO: use the user_id of the user from the token
    data = parse_form_or_body(request)
    async with get_async_session() as session:
        resp = await User.delete_user(session, data["ident"])
    return json(resp)


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


@protected()
@bp.route("login_check")
async def loggedin(request: Request):
    return json({"ok": True, "msg": "you are logged in"})


@bp.route("user_exists", methods=("POST",))
async def user_exists(request):
    data = parse_form_or_body(request)
    ident = data.get("ident")
    async with get_async_session() as session:
        if '@' in ident:
            exists = await User.email_exists(session, ident)
        else:
            exists = await User.username_exists(session, ident)
    return json({"ok": True, "exists": exists})
