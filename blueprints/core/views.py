from sanic.response import json, text
from sanic.blueprints import Blueprint
from utils.auth import isAuthenticated

bp = Blueprint("core", url_prefix="api/core/")


@bp.route("users")
async def users(request):
    print(request.ctx.session)
    print(request.ctx.session["session"])
    print(dir(request.ctx.session["session"]))
    print(request.ctx.session["session"].sid)
    print(request.cookies)
    response = json({"users": ["user1", "user2", "user3", "user4"]})
    response.cookies["hello"] = "world"
    return response


@bp.route("users2")
async def users2(request):
    return json({"users": ["user1", "user2", "user3", "user4", "user5"]})


@bp.route("cookie")
async def cookie(request):
    response = json({"users": ["user1", "user2", "user3", "user4", "user5"]})
    response.cookies['test'] = 'something'
    response.cookies['test']['domain'] = 'localhost'
    response.cookies['test']['samesite'] = 'strict'
    return response


@bp.route("redis_cache")
async def redis_cache(request):
    if not request['session'].get('foo'):
        request['session']['foo'] = 0

    request['session']['foo'] += 1

    response = text(request['session']['foo'])

    return response


@bp.route("login")
async def login(request):
    response = json({"authenticated": True})
    response.cookies["login_token"] = "authenticated"
    response.cookies["login_token"]["samesite"] = "Strict"

    return response


@bp.route("authenticated")
@isAuthenticated
async def profile(request):
    return json({"loggedin": True})


@bp.route("logout")
async def logout(request):
    response = json({"loggedin": True})
    del response.cookies["login_token"]
    return response
