###############################################################################
# Copyright (C) 2020, created on May 23, 2020
# Written by Justin Ho
#
# This source code is provided free of charge and without warranty.
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
###############################################################################

from sanic_wtf import SanicForm
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.orm import model_form

from db.auth import User
from utils.forms import Converter, FormSpec
from wtforms.fields.core import Field


class UserForm(SanicForm, model_form(User, converter=Converter())):
    pass


class LoginForm(SanicForm, FormSpec):
    ident = TextField("username_or_email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])


if __name__ == "__main__":

    userForm = UserForm()
    print(userForm)

    props = vars(userForm)
    for k, v in props.items():
        if isinstance(v, Field):
            print(k, v)

    loginForm = LoginForm()
    loginForm.renderSpec()
