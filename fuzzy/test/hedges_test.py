import math
import unittest

from fuzzy.Hedge import dict_hedges
from fuzzy.MembershipFunction import MembershipFunction


def func(u):
    return 1.0 / (1 + ((u - 10) / 7.0) ** 12)


class MyTestCase(unittest.TestCase):
    mf = MembershipFunction(func)
    hedges = dict_hedges()

    def test_not(self):
        not_h = self.hedges["not"]
        self.mf.hedge = not_h
        for i in range(0, 30):
            self.assertAlmostEqual(1.0 - round(func(i), 2), round(self.mf(i), 2))

    def test_very(self):
        very = self.hedges["very"]
        self.mf.hedge = very
        for i in range(0, 30):
            self.assertAlmostEqual(math.pow(func(i), 2), self.mf(i))

    def test_highly(self):
        highly = self.hedges["highly"]
        self.mf.hedge = highly
        for i in range(0, 30):
            self.assertAlmostEqual(math.pow(math.pow(func(i), 2), 1.25), self.mf(i))


if __name__ == '__main__':
    unittest.main()
