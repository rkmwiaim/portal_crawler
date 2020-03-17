import unittest

from crawler import simple


class SimpleTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def t2est_thoughts(self):
        self.assertIsNone(simple.simple())


if __name__ == '__main__':
    unittest.main()
