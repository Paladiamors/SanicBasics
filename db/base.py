'''
Created on May 17, 2020

@author: justin
'''

import asyncio

from settingsManager import get_settings
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

settingsManager = get_settings()

Base = declarative_base()


class SessionManager:

    connDict = {"memory": "sqlite://",
                "local": f"sqlite:///{settingsManager.base_path}/local.db"}

    asyncConnDict = {"memory": "sqlite+aiosqlite://",
                     "local": f"sqlite+aiosqlite:///{settingsManager.base_path}/local.db"}

    def __init__(self):
        self.engines = {}
        self.sessionMakers = {}
        self.async_engines = {}
        self.async_sessions = {}

    def get_engine(self, env, echo=False):

        if env not in self.engines:
            connString = self.connDict[env]
            engine = create_engine(connString, echo=echo)
            self.engines[env] = engine

        else:
            engine = self.engines[env]

        return engine

    def get_session(self, env, echo=False):

        if env not in self.sessionMakers:
            engine = self.get_engine(env, echo)
            Session = sessionmaker(engine)
            self.sessionMakers[env] = Session

        else:
            Session = self.sessionMakers[env]

        return Session()

    def get_async_engine(self, env, echo=False):

        if env not in self.async_engines:
            connString = self.asyncConnDict[env]
            self.async_engines[env] = create_async_engine(connString, echo=echo)

        return self.async_engines[env]

    def get_async_session(self, env, echo=False):

        if env not in self.async_sessions:
            engine = self.get_async_engine(env, echo)
            Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
            self.async_sessions[env] = Session
        else:
            Session = self.async_sessions[env]
        return self.async_sessions[env]()

    def create_tables(self, env):
        engine = self.get_engine(env)
        Base.metadata.create_all(engine)

    async def create_tables_async(self, env):
        engine = self.get_async_engine(env)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


session_manager = SessionManager()


def get_session(env=None, echo=False):
    if not env:
        from env import env as imported_env
        env = imported_env
    return session_manager.get_session(env, echo=echo)


def get_async_session(env="main", echo=False):
    return session_manager.get_async_session(env=env, echo=echo)


if __name__ == "__main__":

    session_manager.create_tables("memory")
