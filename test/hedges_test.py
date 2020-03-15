import math
import unittest

from Hedge import dict_hedges
from MembershipFunction import MembershipFunction


class MyTestCase(unittest.TestCase):
    mf = MembershipFunction(lambda u: 1.0 / (1 + ((u - 10) / 7.0) ** 12))
    hedges = dict_hedges()

    def test_not(self):
        not_h = self.hedges["not"]
        for i in range(0, 30):
            self.assertAlmostEqual(1.0 - round(self.mf(i), 2), round(not_h.apply(self.mf)(i), 2))

    def test_very(self):
        very = self.hedges["very"]
        for i in range(0, 30):
            self.assertAlmostEqual(math.pow(self.mf(i), 2), very.apply(self.mf)(i))

    def test_highly(self):
        highly = self.hedges["highly"]
        for i in range(0, 30):
            self.assertAlmostEqual(math.pow(math.pow(self.mf(i), 2), 1.25), highly.apply(self.mf)(i))


if __name__ == '__main__':
    unittest.main()
