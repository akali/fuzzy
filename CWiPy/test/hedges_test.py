import math
import unittest

from CWiPy.Modifier import dict_modifiers
from CWiPy.MembershipFunction import MembershipFunction


def func(u):
    return 1.0 / (1 + ((u - 10) / 7.0) ** 12)


class MyTestCase(unittest.TestCase):
    mf = MembershipFunction(func)
    modifiers = dict_modifiers()

    def test_not(self):
        not_h = self.modifiers["not"]
        self.mf.modifier = not_h
        for i in range(0, 30):
            self.assertAlmostEqual(1.0 - round(func(i), 2), round(self.mf(i), 2))

    def test_very(self):
        very = self.modifiers["very"]
        self.mf.modifier = very
        for i in range(0, 30):
            self.assertAlmostEqual(math.pow(func(i), 2), self.mf(i))

    def test_highly(self):
        highly = self.modifiers["highly"]
        self.mf.modifier = highly
        for i in range(0, 30):
            self.assertAlmostEqual(math.pow(math.pow(func(i), 2), 1.25), self.mf(i))


if __name__ == '__main__':
    unittest.main()
