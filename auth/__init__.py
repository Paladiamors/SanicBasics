from sanic.response import json


def authenticated(f):

    def func(request):
        login_token = request.cookies.get("login_token")
        if not login_token:
            return json({"ok": False, "message": "please authenticate"})
        else:
            return f(request)

    return func
