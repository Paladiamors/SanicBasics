'''
Created on May 17, 2020

@author: justin
'''

import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Index
from sqlalchemy_utils import PasswordType, EmailType

from db.base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    password = Column(PasswordType(schemes=["pbkdf2_sha512"]), nullable=False)
    username = Column(String(150), nullable=False, unique=True)
    email = Column(EmailType, nullable=False, unique=True)
    isStaff = Column(Boolean, default=False)
    isActive = Column(Boolean, default=True)
    dateJoined = Column(DateTime(True), default=datetime.datetime.now)
    verified = Column(Boolean, default=False)

    ix_username_email = Index("ix_username_email", username, email)
