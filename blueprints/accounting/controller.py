###############################################################################
# Copyright (C) 2022, created on February 05, 2022
# Written by Justin Ho
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3 as published by
# the Free Software Foundation.
#
# This source code is distributed in the hope that it will be useful and
# without warranty or implied warranty of merchantability or fitness for a
# particular purpose.
###############################################################################

from sqlalchemy import select, and_, Date
from db.accounting import AccountingRecord as Record
from db.auth import User
from db.base import get_async_session
from db.utils import async_dictify

type_map = {Date: lambda x: x.isoformat()}


async def add_record(data):
    record = Record(**data)
    try:
        record = Record(**data)
    except BaseException:
        return {"ok": False}
    async with get_async_session() as session:
        async with session.begin():
            session.add(record)
            await session.commit()
        return {"ok": True}


async def get_records(uid, start_date=None, end_date=None):

    columns = [Record.id, Record.date, Record.type, Record.description, Record.cost, Record.comment]
    query = select(*columns).\
        join(User).\
        filter(User.id == uid)

    if start_date:
        query = query.filter(Record.date >= start_date)
    if end_date:
        query = query.filter(Record.date <= end_date)

    async with get_async_session() as session:
        result = await async_dictify(session, query, type_map=type_map)
    return result


async def delete_record(uid, rid):

    query = Record.__table__.delete().\
        where(and_(Record.id == rid,
                   Record.user_id == uid))
    async with get_async_session() as session:
        async with session.begin():
            await session.execute(query)
            await session.commit()
    return {"ok": True}


async def delete_records(uid, rids):

    query = Record.__table__.delete().\
        where(and_(Record.id.in_(rids),
                   Record.user_id == uid))
    async with get_async_session() as session:
        async with session.begin():
            await session.execute(query)
            await session.commit()
    return {"ok": True}
