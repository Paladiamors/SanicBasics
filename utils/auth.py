'''
Created on May 17, 2020

@author: justin

tools for authentication
'''
from utils.redis import RedisStore
from sanic.response import json


def authenticate(login, password, redisStore):
    """
    simple authentication mechanism
    """
    redisStore.session["authenticated"] = True
    
    return True

def is_authenticated(f):
    """
    decorator for authentication
    decorates a view
    """
    
    def func(request):
        
        dataStore = RedisStore(request)
        if dataStore.session.get("authenticated"):
            return f(request)
        else:
            return json({"ok": False, "msg": "please authenticate"})
    
    return func

def logout(request):
    """
    performs a logout on the request
    """
    
    dataStore =  RedisStore(request)
    if dataStore.session.get("authenticated"):
        response = json({"ok": True})
        del dataStore.session["authenticated"]
        del response.cookies["authenticated"]
        return response
    else:
        return json({"ok": False, "msg": "not logged in"})

def create_user(request, method=["GET", "POST"]):
    """
    creates a user
    """
    
    