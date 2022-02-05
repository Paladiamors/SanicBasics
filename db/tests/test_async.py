import unittest
import aiounittest


class Test(aiounittest.AsyncTestCase):

    async def test_name(self):
        print("running test")


if __name__ == "__main__":
    unittest.main()
