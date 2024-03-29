'''
Created on May 17, 2020

@author: justin
'''

import datetime
from string import ascii_letters, digits

from sqlalchemy import (Boolean, Column, DateTime, Index, Integer, String,
                        select)
from sqlalchemy_utils import PasswordType

from db.base import Base


class User(Base):

    characters = ascii_letters + digits

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(PasswordType(schemes=['pbkdf2_sha512']))
    last_password_reset = Column(DateTime)
    admin = Column(Boolean)
    new_email = Column(String)
    verified = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    joined_on = Column(DateTime, default=datetime.date.today)

    ix_user_email = Index('ix_user_email', email)
    ix_user_username = Index('ix_user_username', username)

    @classmethod
    async def get_user(cls, session, ident):
        """returns the user object if it exists
        else None

        Parameters
        ----------
        session : sqlalcehmy.session
        ident : str
            username or email

        returns True if ther user exists
        """

        if '@' in ident:
            query = select(cls).\
                filter(cls.email == ident)
        else:
            query = select(cls).\
                filter(cls.username == ident)

        cursor = await session.execute(query)
        return cursor.scalar()

    @classmethod
    async def username_exists(cls, session, ident):

        query = select(cls.id).\
            filter(cls.username == ident)
        cursor = await session.execute(query)
        result = cursor.scalar()
        return True if result else False

    @classmethod
    async def email_exists(cls, session, ident):

        query = select(cls.id).\
            filter(cls.email == ident)
        cursor = await session.execute(query)
        result = cursor.scalar()
        return True if result else False

    @classmethod
    async def add_user(cls, session, info):
        errors = []
        async with session.begin():
            username_exists = await cls.username_exists(session, info["username"])
            email_exists = await cls.email_exists(session, info["email"])

            if username_exists:
                errors.append({"error": "Username", "msg": "Username is already taken"})
            if email_exists:
                errors.append({"error": "Email", "msg": "Email already registered"})

            if not errors:
                user = User(**info)
                session.add(user)
                await session.commit()
                return {"ok": True, "msg": "user added"}

        return {"ok": False, "errors": errors}

    @classmethod
    async def delete_user(cls, session, ident):

        async with session.begin():
            user = await cls.get_user(session, ident)
            if user:
                await session.delete(user)
                return {"ok": True, "msg": "user deleted"}

        return {"ok": False, "msg": "user does not exist"}

    @classmethod
    async def authenticate(cls, session, ident, password):

        user = await cls.get_user(session, ident)
        if not user or user.password != password:
            return {"ok": False, "msg": "Username or password is incorrect"}
        else:
            return {"ok": True, "username": user.username, "uid": user.id, "admin": user.admin}

    @classmethod
    async def update_email(cls, session, old_email, new_email):
        async with session.begin():
            query = cls.__table__.update().\
                where(cls.email == old_email).\
                values(email=new_email)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update_username(cls, session, old_username, new_username):
        async with session.begin():
            query = cls.__table__.update().\
                where(cls.username == old_username).\
                values(username=new_username)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def verify_user(cls, session, email):
        async with session.begin():
            query = cls.__table__.update().\
                where(cls.email == email).\
                values(verified=True)
            await session.execute(query)
            await session.commit()
