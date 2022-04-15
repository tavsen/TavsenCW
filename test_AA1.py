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

    def test_remove_val(self):
        self.AA.add(12)
        self.AA.add(23)
        self.AA.remove(23)
        self.assertEqual(self.AA.root.val, 12)

    def test_remove_val_more_then_2(self):
        self.AA.add(12)
        self.AA.add(23)
        self.AA.add(24)
        self.AA.remove(23)
        self.assertEqual(self.AA.root.val, 12)
        self.assertEqual(self.AA.root.right.val, 24)

    def test_max(self):
        self.AA.add(12)
        self.AA.add(23)
        self.AA.add(34)
        self.AA.max()
        self.assertEqual(self.AA.max(), 34)

    def test_min(self):
        self.AA.add(12)
        self.AA.add(23)
        self.AA.add(34)
        self.AA.min()
        self.assertEqual(self.AA.min(), 12)

    def test_forward_from(self):
        self.AA.add(12)
        self.AA.add(23)
        self.AA.add(34)
        self.AA.forward_from(12)


if __name__ == '__main__':
    pass
