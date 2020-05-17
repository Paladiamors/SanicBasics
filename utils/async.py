###############################################################################
# Copyright (C) 2022, created on January 30, 2022
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

# helper function to allow function to run as async function

import asyncio
from functools import wraps


def maybeasync(f):
    """Decorator that allows a function to run as maybe async code"""
    loop = asyncio.get_event_loop()

    @wraps(f)
    def wrap(*args):
        if loop.is_running():
            return loop.run_in_executor(None, f, *args)
        else:
            return f(*args)
    return wrap
