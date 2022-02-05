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
import asyncio
import datetime
import unittest

import aiounittest
from _env_test import env
from decimal import Decimal
from blueprints.accounting.controller import add_record as add_record_
from blueprints.accounting.controller import delete_record as delete_record_
from blueprints.accounting.controller import delete_records as delete_records_
from blueprints.accounting.controller import get_records as get_records_
from db.base import get_async_session, session_manager
from db.auth import User
from sqlalchemy import select
from db.tests.utils import create_user


class Test(aiounittest.AsyncTestCase):

    def setUp(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(session_manager.create_tables_async(env))

    async def test_name(self):

        await create_user()
        async with get_async_session() as session:
            query = select(User)
            cursor = await session.execute(query)
            user = cursor.scalar()
            user_id = user.id
        record = {"user_id": user_id, "cost": 100, "date": datetime.date.today()}
        result = await add_record_(record)
        self.assertTrue(result["ok"])

        record = {"user_id": user_id, "cost": 100, "date": datetime.date.today()}
        result = await add_record_(record)
        self.assertTrue(result["ok"])

        result = await get_records_(1)
        expected_results = [{'id': 1,
                             'date': '2022-02-05',
                             'type': None,
                             'description': None,
                             'cost': Decimal('100.00'),
                             'comment': None},
                            {'id': 2,
                             'date': '2022-02-05',
                             'type': None,
                             'description': None,
                             'cost': Decimal('100.00'),
                             'comment': None}]

        self.assertEqual(result, expected_results)

        result = await delete_record_(1, 1)
        self.assertTrue(result["ok"])

        result = await get_records_(1)
        self.assertEqual(len(result), 1)

        result = await delete_records_(1, [2])
        self.assertTrue(result["ok"])

        result = await get_records_(1)
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()
