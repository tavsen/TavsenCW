import unittest
from AA import sbst


class AATest(unittest.TestCase):
    def setUp(self):
        self.AA = sbst()

    def test_addval(self):
        self.AA.add(12)
        self.assertEqual(self.AA.root.val, 12)

    def test_addval_neg(self):
        self.AA.add(-12)
        self.assertEqual(self.AA.root.val, -12)

    def test_addval_float(self):
        self.AA.add(12.3)
        self.assertEqual(self.AA.root.val, 12.3)

    def test_addval_mul(self):
        self.AA.add(12)
        self.AA.add(23)
        self.assertEqual(self.AA.root.val, 12)
        self.assertEqual(self.AA.root.right.val, 23)
        
    def test_remove_last_val(self):
        self.AA.add(12)
        self.AA.remove(12)
        self.assertEqual(self.AA.root, None)


if __name__ == '__main__':
    pass
