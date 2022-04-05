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
    # def test_backward_from(self):
    #     self.AA.add(12)
    #     self.AA.add(23)
    #     self(*[v for v in self.forward_from(2))
    #     self.assertEqual(self.AA.backward_from(), 23, 12)

    # def test_addval_multiple(self):
    #     self.AA.add(10)
    #     self.AA.add(13)
    #     self.AA.add(12)
    #     self.assertEqual(self.AA.val, 10, self.AA.val,12, 13)



if __name__ == '__main__':
    pass