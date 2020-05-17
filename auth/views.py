from sanic.response import json
from sanic import Blueprint

bp = Blueprint("auth")

@bp.route("/login")
async def login(request, methods=["GET","POST"]):
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
