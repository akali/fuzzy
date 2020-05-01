import unittest
from CWiPy import MembershipFunction as mf
from CWiPy.Modifier import dict_modifiers


class TestRangeExtraction(unittest.TestCase):
    triangle_mf = mf.TriangularMembershipFunction(0, 10, 20)
    trap_mf = mf.TrapezoidMembershipFunction(0, 10, 20, 30)

    def test_triangle(self):
        l, r = self.triangle_mf.extract_range(0.5)
        self.assertAlmostEqual(5, l)
        self.assertAlmostEqual(15, r)

    def test_trapezoid(self):
        l, r = self.trap_mf.extract_range(0.5)
        self.assertAlmostEqual(5, l)
        self.assertAlmostEqual(25, r)

    def test_trapezoid_with_very(self):
        modifiers = dict_modifiers()
        very = modifiers['very']
        self.trap_mf.set_modifier(very)
        l, r = self.trap_mf.extract_range(0.5)
        print('very', l, r)
        self.assertAlmostEqual(7.071067804794407, l)
        self.assertAlmostEqual(22.928932195205594, r)
        self.trap_mf.set_modifier(None)


if __name__ == '__main__':
    unittest.main()
