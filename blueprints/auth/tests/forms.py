'''
Created on May 17, 2020

@author: justin
'''


user = [{"key": "username", "required": True, "type": str},
        {"key": "password", "required": True, "type": str},
        {"key": "email", "required": True, "type": str},
        {"key": "is_staff", "required": False, "type": bool, "default": False},
        {"key": "is_active", "required": False, "type": bool, "default": True},
        ]