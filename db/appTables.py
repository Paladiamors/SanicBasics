'''
Created on May 17, 2020

@author: justin
'''

from db.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy_utils import PasswordType, EmailType

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    password = Column(PasswordType(schemes=["pbkdf2_sha512"]), nullable=False)
    username = Column(String(150), nullable=False, unique=True)
    email = Column(EmailType, nullable=False)
    is_staff = Column(Boolean, nullable=False)
    is_active = Column(Boolean, nullable=False)
    date_joined = Column(DateTime(True), nullable=False)
    verified = Column(Boolean, default=False)
    
    

