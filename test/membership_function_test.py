import unittest
import MembershipFunction as mf


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


if __name__ == '__main__':
    unittest.main()
