'''
Created on May 17, 2020

@author: justin
'''

import copy
import datetime
from random import randint
import time

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

# connDict = {"main": "postgresql+psycopg2://service:service@paladiamors.com/Stocks",
#             "test": "postgresql+psycopg2://service:service@paladiamors.com/Stocks_test"}

connDict = {"main": "postgresql+psycopg2://service:service@paladiamors.com/SanicApp",
            "memory": "sqlite://"}

Base = declarative_base()


class SessionManager:

    def __init__(self):
        self.engines = {}
        self.sessionMakers = {}

    def getEngine(self, env, echo=False):

        if env not in self.engines:
            connString = connDict[env]
            engine = create_engine(connString, echo=echo)
            self.engines[env] = engine

        else:
            engine = self.engines[env]

        return engine

    def getSession(self, env, echo=False):

        if env not in self.sessionMakers:
            engine = self.getEngine(env, echo)
            Session = sessionmaker(engine)
            self.sessionMakers[env] = Session

        else:
            Session = self.sessionMakers[env]

        return Session()

    def createTables(self, env):

        engine = self.getEngine(env)
        Base.metadata.create_all(engine)

    def memorySession(self):

        env = "memory"
        self.createTables(env)
        return self.getSession(env)


sessionManager = SessionManager()


def getSession(env):
    return sessionManager.getSession(env)


def memorySession():
    return sessionManager.memorySession()
