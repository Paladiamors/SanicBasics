'''
Created on May 18, 2020

@author: justin
'''
import unittest
from utils.forms import Form


class MockForm(Form):

    fields = [{"key": "username", "required": True, "type": str},
              {"key": "email", "required": False, "type": str},
              {"key": "age", "required": False, "type": int},
              {"key": "height", "required": False, "type": float},
              {"key": "is_staff", "required": False, "type": bool, "default": False},
              {"key": "is_active", "required": False, "type": bool, "default": True},
              ]


class MockRequest:

    def __init__(self, data):
        self.form = data


class Test(unittest.TestCase):

    def test_formParser(self):

        data = {"username": ["bob"]}
        request = MockRequest(data)

        form = MockForm(request)

        result = form.parse()
        errors = form.errors()

        expectedResult = {'username': 'bob', 'is_staff': False, 'is_active': True}
        expectedErrors = []

        self.assertEqual(result, expectedResult, "result should be the same")
        self.assertEqual(errors, expectedErrors, "error should be the same")

    def test_missing(self):

        request = MockRequest({})
        form = MockForm(request)

        result = form.parse()
        errors = form.errors()

        expectedResult = {}
        self.assertEqual(result, expectedResult, "result should be the same")
        self.assertTrue(errors, "there should be an error")

    def test_badValue(self):

        data = {"username": ["bob"], "age": ["oops"]}
        request = MockRequest(data)
        form = MockForm(request)

        result = form.parse()
        errors = form.errors()

        expectedResult = {}
        self.assertEqual(result, expectedResult, "result should be the same")
        self.assertTrue(errors, "there should be an error")

        print(errors)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test']
    unittest.main()
