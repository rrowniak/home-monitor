import unittest

import utils

class TestUtilsFunctions(unittest.TestCase):
    def test_callCmd(self):
        c, out, err = utils.callCmd(['ls'])
        self.assertEqual(c, 0)
        self.assertGreater(len(out), 0)

if __name__ == '__main__':
    unittest.main()