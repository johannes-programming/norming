import unittest

__all__ = ["test"]


def test() -> unittest.TextTestRunner:
    "This function runs all the tests."
    loader: unittest.TestLoader
    suite: unittest.TestSuite
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="norming.tests")
    return unittest.TextTestRunner().run(suite)
