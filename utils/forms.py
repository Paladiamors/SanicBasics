'''
Created on May 17, 2020

@author: justin
'''


def parseForm(request):
    """
    naive form parser
    """

    if not request.form:
        return {}

    data = {k: v[0] for k, v in request.form.items()}
    return data


class Form:
    """
    base class to parse a form
    """

    # this needs to be overriden
    fields = []

    def __init__(self, request):

        self.request = request

    def parse(self):
        """
        parses the form
        """

        pass

    def spec(self):
        """
        returns the spec of the form for rendering
        """

        pass
