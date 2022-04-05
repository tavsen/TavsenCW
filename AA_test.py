import unittest
from AA import sbst


class AATest(unittest.TestCase):
    def setUp(self):
        self.AA = sbst()
    def test_addval(self):
        self.AA.add(12)
        self.assertEqual(self.AA.root.val, 12)
    def test_addnval_neg(self):
        self.AA.add(-12)
        self.assertEqual(self.AA.root.val, -12)
    def test_addval_float(self):
        self.AA.add(12.3)
        self.assertEqual(self.AA.root.val, 12.3)
    def test_addval_none(self):
        self.AA.add(None)
        self.assertEqual(self.AA.root.val, None)

if __name__ == '__main__':
    pass
