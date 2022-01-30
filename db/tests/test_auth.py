import asyncio
import unittest
from db.auth import User
from db.base import get_async_session, session_manager

env = "memory"


class Test(unittest.TestCase):

    def setUp(self) -> None:
        asyncio.run(self.asyncSetup())

    async def asyncSetup(self):
        await session_manager.create_tables_async(env)

    async def add_user_async(self):
        info = {"username": "testUser", "password": "12345", "email": "test@test.com"}
        async with get_async_session(env=env) as session:
            await User.add_user(session, info)
            self.assertTrue(await User.username_exists(session, "testUser"))
            self.assertTrue(await User.email_exists(session, "test@test.com"))

        async with get_async_session(env=env) as session:
            resp = await User.authenticate(session, "test@test.com", "12345")
            self.assertTrue(resp["ok"])

        async with get_async_session(env=env) as session:
            await User.delete_user(session, "test@test.com")
            self.assertFalse(await User.username_exists(session, "testUser"))

    def test_add_user_async(self):
        asyncio.run(self.add_user_async())


if __name__ == "__main__":
    unittest.main()
