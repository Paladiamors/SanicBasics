###############################################################################
# Copyright (C) 2020, created on May 23, 2020
# Written by Justin Ho
#
# This source code is provided free of charge and without warranty.
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
###############################################################################


import datetime
import os
from functools import wraps
from random import randint

import pandas
from sqlalchemy import (Column, MetaData, PrimaryKeyConstraint, Table, and_,
                        func, select)
from sqlalchemy.sql.selectable import Select


def optional_session(f):
    """ wraps a class method to allow use with an optional session """
    @wraps(f)
    def wrapper(cls, *args, env=None, session=None, **kwargs):
        if session:
            return f(cls, session, *args, **kwargs)
        else:
            with cls.get_session(env=env) as session:
                return f(cls, session, *args, **kwargs)
    return wrapper


def SessionMixinFactory(context_func):
    """ context_func is a function that creates a session context
    This function returns a SessionMixin class that is bound to a session context
    Also adds some handy helper classes"""
    class SessionMixin:
        @staticmethod
        def get_session(env=None):
            return context_func(env)

        @staticmethod
        def now():
            return datetime.datetime.utcnow()

    return SessionMixin


def bulk_insert(session, table, data):
    """
    performs a bulk insert into the table
    """
    with session.begin():
        session.bulk_insert_mappings(table, data)


def create_temp_table(table):

    table_name = "temp_%s_%s" % (table.__tablename__, f"{os.getpid()}_{randint(0, 10000)}")
    new_table = table.__table__.to_metadata(table.metadata, name=table_name)
    new_table.indexes = set()
    return new_table


def create_temp_table_orig(session, table, parentTable=None, mappingCols=[]):

    # metadata = copy.copy(table.metadata)
    metadata = MetaData()
    metadata.bind = session.bind
    cols = [c.copy() for c in table.__table__.columns]
    constraints = [c.copy() for c in table.__table__.constraints if not isinstance(c, PrimaryKeyConstraint)]

    if parentTable and mappingCols:
        for col in mappingCols:
            cols.append(Column(col, parentTable.__table__.c[col].type))

    return Table("temp_%s_%s" % (table.__tablename__,
                                 f"{os.getpid()}_{randint(0, 10000)}"), metadata, *(cols + constraints))


def unique_upsert(session, table, data, uniqueColumns):

    if not data:
        return

    tableClone = create_temp_table(table)
    with session.bind.begin() as engine:
        tableClone.create(bind=engine)

    try:
        ins = tableClone.insert().values(data)
        with session.begin():
            session.execute(ins)

        keys = [key for key in data[0].keys() if key in table.__table__.c]

        updateColumnNames = set(keys).difference(set(uniqueColumns))

        updateColumns = {name: getattr(tableClone.c, name) for name in updateColumnNames}
        whereClause = and_(*[getattr(table.__table__.c, col) == getattr(tableClone.c, col) for col in uniqueColumns])

        # perform the update
        updateQuery = table.__table__.update().\
            values(**updateColumns).\
            where(whereClause)

        # perform the insert
        cols = [getattr(tableClone.c, name) for name in keys] + \
            [getattr(table.__table__.c, uniqueColumns[0]).label("DDUMMY")]

        stmt = select(*cols).\
            outerjoin(table, whereClause).\
            subquery()

        insertStmt = select(*stmt.c.values()[:-1]).\
            filter(stmt.c.DDUMMY.is_(None))
        insertQuery = table.__table__.insert().from_select(cols[:-1], insertStmt)

        with session.begin():
            session.execute(updateQuery)
            session.execute(insertQuery)

    except BaseException:
        with session.bind.begin() as engine:
            tableClone.drop(bind=engine)
        raise

    with session.bind.begin() as engine:
        tableClone.drop(bind=engine)


def duplicate_query(session, table, partition, as_subquery=False):
    """returns either a query or subquery to detect duplicates in a table

    Parameters
    ----------
    session : sqlalchemy session
        session to database
    table : table
        database table
    partition : list[str]
        list of strings representing the columns to act as partition
    as_subquery : bool, optional
        if true returns as subquery otherwise returns as query object, by default False

    Returns
    -------
    query or subquery
        used to display duplicate data or subquery to delete data
    """
    columns = [getattr(table, attrib) for attrib in partition]
    dupes = session.query(*columns, func.count(columns[0]).label("count")).\
        group_by(*columns).\
        subquery()

    if len(columns) == 1:
        join_cond = getattr(table, partition[0]) == getattr(dupes.c, partition[0])
    else:
        joins = [getattr(table, attrib) == getattr(dupes.c, attrib) for attrib in partition]
        join_cond = and_(*joins)
    details = session.query(table.id, *columns,
                            func.rank().over(
                                order_by=table.id,
                                partition_by=columns).label("ranking")).\
        join(dupes, join_cond).\
        filter(dupes.c.count > 1)

    if not as_subquery:
        return details.order_by(*columns)
    else:
        return details.subquery()


def duplicate_delete(session, table, partition):
    """ Use this query to delete duplicate data from a table """

    details = duplicate_query(session, table, partition, True)

    delete_query = table.__table__.delete().\
        where(and_(table.id == details.c.id,
                   details.c.ranking > 1))

    session.execute(delete_query)
    session.commit()


def dictify(session, query: Select, type_map=None):
    """
    used to convert a query or subquery into a dictionary
    """

    columns = [col["name"] for col in query.column_descriptions]
    data = [dict(list(zip(columns, row))) for row in session.execute(query).all()]

    if type_map:
        for row in data:
            for col in query.column_descriptions:
                if type(col["type"]) in type_map:
                    row[col["name"]] = type_map[type(col["type"])](row[col["name"]])
    return data


async def async_dictify(session, query: Select, type_map=None):
    """
    used to convert a query or subquery into a dictionary
    """

    columns = [col["name"] for col in query.column_descriptions]
    response = await session.execute(query)
    data = [dict(list(zip(columns, row))) for row in response.all()]

    if type_map:
        for row in data:
            for col in query.column_descriptions:
                if type(col["type"]) in type_map:
                    row[col["name"]] = type_map[type(col["type"])](row[col["name"]])
    return data


def toDf(session, query: Select, underbarAsSpace=False, type_map=None):
    """
    returns the data from the database as a dataframe
    """

    if isinstance(query, Select):

        columns = [col["name"] for col in query.column_descriptions]
        if underbarAsSpace:
            columns = [col.replace("_", " ") for col in columns]
        data = pandas.DataFrame(session.execute(query).all(), columns=columns)

    else:
        raise("unknown query object to handle")

    if type_map:
        for name, col in query.columns.items():
            if type(col.type) in type_map:
                data.loc[:, name] = data.loc[:, name].apply(type_map[type(col.type)])

    return data


async def async_toDf(session, query: Select, underbarAsSpace=False, type_map=None):
    """
    returns the data from the database as a dataframe
    """

    if isinstance(query, Select):

        columns = [col["name"] for col in query.column_descriptions]
        if underbarAsSpace:
            columns = [col.replace("_", " ") for col in columns]
        response = await session.execute(query)
        data = pandas.DataFrame(response.all(), columns=columns)

    else:
        raise("unknown query object to handle")

    if type_map:
        for name, col in query.columns.items():
            if type(col.type) in type_map:
                data.loc[:, name] = data.loc[:, name].apply(type_map[type(col.type)])

    return data
