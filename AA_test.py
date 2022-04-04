import unittest
from AA import sbst


class AATest(unittest.TestCase):
    def setUp(self):
        self.AA = sbst()

class Test_add(AATest):
    def test_add_val(self):
        self.AA.add(12)
        self.assertEqual(self.AA.add(12), None)
    def test_add_negval(self):
        self.AA.add(-12)
        self.assertEqual(self.AA.add(-12), None)
    def test_add_floatval(self):
        self.AA.add(12.3)
        self.assertEqual(self.AA.add(-12), None)


if __name__ == '__main__':
    unittest.main()