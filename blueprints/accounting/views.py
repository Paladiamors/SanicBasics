###############################################################################
# Copyright (C) 2022, created on February 05, 2022
# Written by Justin Ho
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3 as published by
# the Free Software Foundation.
#
# This source code is distributed in the hope that it will be useful and
# without warranty or implied warranty of merchantability or fitness for a
# particular purpose.
###############################################################################
import datetime
from sanic.blueprints import Blueprint
from sanic.request import Request
from sanic.response import json
from sanic_jwt.decorators import protected
from utils.encrypt import decode_token

from .controller import add_record as add_record_
from .controller import delete_record as delete_record_
from .controller import delete_records as delete_records_
from .controller import get_records as get_records_

bp = Blueprint("accounting", url_prefix="accounting/")


@bp.route("add_record", methods=["GET", "POST"])
@protected()
async def add_record(request: Request):
    if request.method == "POST":
        token = decode_token(request)
        record = request.json
        record["user_id"] = token["user_id"]
        result = await add_record_(record)
        return json(result)
    else:
        return json({"ok": False, "msg": "GET not allowed"})


@bp.route("get_records")
@protected()
async def get_records(request: Request):
    token = decode_token(request)

    start_date = request.args.get("start_date", None)
    end_date = request.args.get("end_date", None)
    if start_date:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    if end_date:
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    response = await get_records_(token["user_id"], start_date=start_date, end_date=end_date)
    return json(response)


@bp.route("delete_record", methods=["GET", "POST"])
@protected()
async def delete_record(request: Request):
    token = decode_token(request)

    rid = request.args.get("rid", None)
    return await delete_record_(token["user_id"], rid)


@bp.route("delete_records", methods=["GET", "POST"])
@protected()
async def delete_records(request: Request):
    token = decode_token(request)

    rids = request.args.get("rids", None)
    return await delete_records_(token["user_id"], rids)
