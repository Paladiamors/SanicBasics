###############################################################################
# Copyright (C) 2022, created on January 31, 2022
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
import json


def parse_form(request):
    """basic form parser"""

    if request.method == "POST":
        return {k: v[0] for k, v in request.form.items()}
    else:
        return {}


def parse_body(request):
    """basic form parser"""

    if request.method == "POST":
        try:
            return json.loads(request.body.decode("utf-8"))
        except json.decoder.JSONDecodeError:
            return {}
    else:
        return {}


def parse_form_or_body(request):
    """parses a form or body"""

    if request.method == "POST":
        if result := parse_form(request):
            return result
        else:
            return parse_body(request)
