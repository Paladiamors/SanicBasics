###############################################################################
# Copyright (C) 2020, created on May 23, 2020
# Written by Justin Ho
# 
# This source code is provided free of charge and without warranty.
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
###############################################################################

from sanic_wtf import SanicForm
from db.appTables import User
from wtforms_sqlalchemy.orm import model_form
from utils.forms import Converter
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired
    
class UserForm(SanicForm, model_form(User,converter=Converter())):
    pass

class LoginForm(SanicForm):
    ident = TextField("username_or_email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    
if __name__ == "__main__":
    
    userForm = UserForm()
    print(userForm)
    print(userForm.Meta.csrf)
    