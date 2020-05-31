'''
Created on May 17, 2020

@author: justin
'''

from wtforms_sqlalchemy.orm import ModelConverter, converts
from wtforms import fields as f

class Converter(ModelConverter):
    """
    The ModelConverter needs to be extended
    when sqlalchemy_utils is used to add additional
    handlers
    """

    @converts('String', 'Unicode', 'PasswordType', 'EmailType')
    def conv_String(self, field_args, **extra):
        self._string_common(field_args=field_args, **extra)
        return f.TextField(**field_args)
    
