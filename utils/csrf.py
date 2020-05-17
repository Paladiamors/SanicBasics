'''
Created on May 17, 2020

@author: justin
'''
import uuid
import datetime
from utils.session import get_request_session


def add_csrf(f):
    """
    adds a csrf token to the session
    """

    def func(request):
        token = uuid.uuid4().hex

        expiry = datetime.datetime.utcnow() + datetime.timedelta(0, 1800)
        expiry_ts = expiry.timestamp()

        session = get_request_session(request)
        csrf = session.get("csrf", {})
        csrf[token] = expiry_ts
        session["csrf"] = csrf

        return f(request)

    return func


def csrf_ok(request, csrf):
    """
    request: (request object)
        the request object
    csrf: (str)
        the csrf token
    """

    ts = get_request_session(request).get(csrf)
    if ts and ts > datetime.datetime.utcnow():
        return True
    else:
        return False
