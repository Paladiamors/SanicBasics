###############################################################################
# Copyright (C) 2020, created on May 23, 2020
# Written by Justin Ho
#
# This source code is provided free of charge and without warranty.
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
###############################################################################

from sanic.response import json
from sanic.blueprints import Blueprint
from sanic_wtf import SanicForm

bp = Blueprint("forms", url_prefix="api/forms/")


class TokenForm(SanicForm):
    pass


@bp.route("token")
def token(request):
    """
    generates a token for the user
    """
    form = TokenForm(request)
    return json({"csrf_token": form.csrf_token._value()})


if __name__ == "__main__":

    pass
