###############################################################################
# Copyright (C) 2020, created on May 23, 2020
# Written by Justin Ho
# 
# This source code is provided free of charge and without warranty.
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
###############################################################################


from sqlalchemy.orm.query import Query
from sqlalchemy.sql import or_
import pandas


def dictify(query):
    """
    used to convert a query or subquery into a dictionary
    """

    if type(query) == Query:

        columns = [col["name"] for col in query.column_descriptions]
        data = [dict(list(zip(columns, row))) for row in query.all()]

    else:
        raise("unknown query object to handle")

    return data


def bulkInsert(session, table, data):

    ins = table.__table__.insert()
    session.execute(ins, data)
    session.commit()


def toDf(query, underbarAsSpace=False):
    """
    returns the data from the database as a dataframe
    """

    if type(query) == Query:

        columns = [col["name"] for col in query.column_descriptions]
        if underbarAsSpace:
            columns = [col.replace("_", " ") for col in columns]
        data = pandas.DataFrame(query.all(), columns=columns)

    else:
        raise("unknown query object to handle")

    return data


def queryFilter(query, subquery, **kwargs):
    """
    does a filter on the query

    query = the query object
    subquery = the subquery table object
    kwargs = dictionary of parameters for the query
    """

    for k, v in kwargs.items():
        cmd, _, key = k.partition("_")
        if cmd == "min":
            query = query.filter(getattr(subquery.c, key) < v)
        elif cmd == "max":
            query = query.filter(getattr(subquery.c, key) > v)
        elif cmd == "or":
            or_query = or_(*[getattr(subquery.c, key) == val for val in v])
            query = query.filter(or_query)
        else:
            query = query.filter(getattr(subquery.c, key) == v)

    return query

def removeDuplicates(dictList, uniqueColumns):
    """
    dictList = list of dicts
    uniqueColumns = the columns the data is to be unique by
    does a naieve method of removing duplicates
    """
    
    index = {}
    for row in dictList:
        i = (row[col] for col in uniqueColumns)
        index[i] = row
    
    return list(index.values())