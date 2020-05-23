'''
Created on May 17, 2020

@author: justin
'''


def parseForm(request):
    """
    naive form parser
    """
    # TODO: escape the dangerous characters.
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
        self.fieldMap = {field["key"]: field for field in self.fields}
        self._errors = []

    def parse(self):
        """
        parses the form and returns the form if the fields are valid
        if the form is not valid, then returns an empty dictionary
        """

        data = {k: v[0] for k, v in self.request.form.items()}
        data = self._parseFields(data)
        data = self._missingFields(data)
        data = self._setDefault(data)

        return data if not self._errors else {}

    def errors(self):
        """
        returns the errors
        """
        return self._errors

    def _parseFields(self, data):
        """
        data is a dictionary
        """

        # TODO: boolean do not send back data if the field unchecked
        for k, v in data.items():
            if isinstance(v, self.fieldMap[k]["type"]):
                # do nothing
                pass
            else:
                try:
                    v = self.fieldMap[k]["type"](v)
                except ValueError:
                    self._errors.append({k: f"Error parsing {v} expected {str(self.fieldMap[k]['type'])}"})

        return data

    def _missingFields(self, data):

        requiredFields = {field["key"] for field in self.fields if field.get("required")}
        formFields = set(data.keys())
        missingFields = requiredFields.difference(formFields)

        if missingFields:
            for field in missingFields:
                self._errors.append({field: "field is missing"})

        return data

    def _setDefault(self, data):

        defaultFields = {field["key"] for field in self.fields if field.get("default") is not None}
        formFields = set(data.keys())
        missingFields = defaultFields.difference(formFields)
        for field in missingFields:
            value = self.fieldMap[field]["default"]
            data[field] = value if not callable(value) else value

        return data

    def spec(self):
        """
        returns the spec of the form for rendering
        """

        pass
