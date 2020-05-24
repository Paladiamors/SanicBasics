'''
Created on May 17, 2020

@author: justin
'''
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker

from settingsManager import settingsManager

connDict = {"main": "postgresql+psycopg2://service:service@paladiamors.com/SanicApp",
            "memory": "sqlite://",
            "local":  f"sqlite:///{settingsManager.basePath}/local.db"}

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


def getSession(env=None, session=None):
    """
    env = environment to make the dconnection
    or use some session already provided
    """
    env = env or settingsManager.getSetting("ENV")
    print("env is", env)
    return session or sessionManager.getSession(env)


def memorySession():
    return sessionManager.memorySession()


if __name__ == "__main__":
    
    sessionManager.createTables("local")