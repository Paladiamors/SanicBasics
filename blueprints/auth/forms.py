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
from wtforms_sqlalchemy.orm import model_form, ModelConverter, converts
from wtforms import fields as f


class Converter(ModelConverter):
    
    @converts('String', 'Unicode', 'PasswordType', 'EmailType')
    def conv_String(self, field_args, **extra):
        self._string_common(field_args=field_args, **extra)
        return f.TextField(**field_args)
    
class UserForm(SanicForm, model_form(User,converter=Converter())):
    pass

if __name__ == "__main__":
    
    userForm = UserForm()
    print(userForm)
    print(userForm.Meta.csrf)
    