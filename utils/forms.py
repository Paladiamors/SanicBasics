'''
Created on May 17, 2020

@author: justin

Comment on how to co
'''

from wtforms_sqlalchemy.orm import ModelConverter, converts
from wtforms import fields as f
from wtforms.fields.core import Field


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


class FormSpec:
    """
    creates the form specifications
    """

    def _getFields(self):
        fieldDict = {k: v for k, v in vars(self).items() if isinstance(v, Field)}
        return fieldDict

    def renderSpec(self):
        """
        returns the spec of the form
        """

        from pprint import pprint
        pprint(self._getFields())
